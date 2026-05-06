console.log('ORACLE loaded');

document.addEventListener('DOMContentLoaded', function() {

  // Wire example buttons
  document.querySelectorAll('.example-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var text = btn.getAttribute('data-text');
      var input = document.getElementById('decision-input');
      input.value = text;
      autoGrow(input);
    });
  });

  // Wire textarea auto-grow
  var textarea = document.getElementById('decision-input');
  textarea.addEventListener('input', function() { autoGrow(this); });

  // Wire consult button
  document.getElementById('consult-btn').addEventListener('click', startAnalysis);

  // Wire new decision button
  document.getElementById('new-decision-btn').addEventListener('click', resetApp);

});

function autoGrow(el) {
  el.style.height = '5px';
  el.style.height = el.scrollHeight + 'px';
}

function setProgress(pct) {
  document.getElementById('progress-bar').style.width = pct + '%';
}

function setStatus(text) {
  var el = document.getElementById('pipeline-status');
  if (text) {
    el.style.display = 'block';
    el.textContent = text;
  } else {
    el.style.display = 'none';
  }
}

function startAnalysis() {
  var decision = document.getElementById('decision-input').value.trim();
  if (!decision) {
    document.getElementById('divider-line').style.background = 'rgba(201,168,76,0.5)';
    setTimeout(function() {
      document.getElementById('divider-line').style.background = 'rgba(255,255,255,0.07)';
    }, 1000);
    return;
  }

  // Show results section
  document.getElementById('input-section').classList.add('hidden');
  document.getElementById('results-section').classList.remove('hidden');
  document.getElementById('decision-display').textContent = decision;
  setProgress(5);

  var stepOrder = ['cartograph','historian','simulate','challenge','reframe','synthesize'];
  var stepLabels = {
    cartograph: 'CARTOGRAPHER — mapping decision space...',
    historian:  'HISTORIAN — analyzing historical base rates...',
    simulate:   'SIMULATOR — projecting consequences...',
    challenge:  'DEVIL\'S ADVOCATE — stress-testing assumptions...',
    reframe:    'REFRAMER — finding the third option...',
    synthesize: 'ORACLE — finalizing verdict...'
  };

  var url = '/api/analyze?decision=' + encodeURIComponent(decision);
  var source = new EventSource(url);

  source.onopen = function() { console.log('SSE connected'); };

  source.onerror = function(e) {
    console.error('SSE error', e);
    setStatus('Connection error — please try again');
  };

  source.onmessage = function(e) {
    try {
      var msg = JSON.parse(e.data);
      console.log('SSE message:', msg.step, msg.status);

      var idx = stepOrder.indexOf(msg.step);
      if (idx >= 0) {
        var pct = ((idx + 1) / stepOrder.length) * 90;
        setProgress(pct);
        setStatus(stepLabels[msg.step] || msg.step);
      }

      if (msg.status === 'complete' && msg.data) {
        renderAgentResult(msg.step, msg.data);
      }

      if (msg.step === 'complete') {
        setProgress(100);
        setStatus(null);
        document.getElementById('new-decision-btn').classList.remove('hidden');
        source.close();
      }

      if (msg.step === 'error') {
        showError(msg.message);
        source.close();
      }

    } catch(err) {
      console.error('JSON parse error:', err, e.data);
    }
  };
}

function showSection(id) {
  var el = document.getElementById(id);
  if (el) {
    el.classList.remove('hidden');
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function showError(message) {
  var el = document.getElementById('section-verdict');
  el.innerHTML = '<div class="error-card">ERROR: ' + (message || 'Unknown error') + '</div>';
  showSection('section-verdict');
}

function renderAgentResult(step, data) {
  if (step === 'cartograph' && data.cartography) renderCartographer(data.cartography);
  if (step === 'historian'  && data.precedents)  renderHistorian(data.precedents);
  if (step === 'simulate'   && data.simulation)  renderSimulator(data.simulation);
  if (step === 'challenge'  && data.devils_advocate) renderAdvocate(data.devils_advocate);
  if (step === 'reframe'    && data.reframe)     renderReframer(data.reframe);
  if (step === 'synthesize' && data.synthesis)   renderVerdict(data.synthesis);
}

function makeSection(label, innerHTML) {
  return '<div class="section-label">' + label + '</div>'
       + '<div class="section-rule"></div>'
       + innerHTML;
}

function renderCartographer(d) {
  var html = makeSection('CARTOGRAPHER — DECISION MAP',
    '<div class="quote-text">"' + esc(d.decision_restated || '') + '"</div>'
    + '<div class="plain-text" style="margin-bottom:0.5rem"><span style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:var(--text-3);letter-spacing:2px">STAKEHOLDERS &nbsp;</span>' + esc((d.stakeholders||[]).join(', ')) + '</div>'
    + '<div class="plain-text" style="margin-bottom:1.5rem"><span style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:var(--text-3);letter-spacing:2px">DOMAINS &nbsp;</span>' + esc((d.domains||[]).join(', ')) + '</div>'
    + '<div class="section-label" style="margin-bottom:0.75rem">HIDDEN ASSUMPTIONS</div>'
    + (d.hidden_assumptions||[]).map(function(a,i) {
        return '<div class="assumption-item">' + (i+1) + '. ' + esc(a) + '</div>';
      }).join('')
    + '<div class="data-label" style="margin-top:1.5rem">' + esc((d.decision_type||'').toUpperCase().replace(/_/g,' · ')) + '</div>'
  );
  var el = document.getElementById('section-cartographer');
  el.innerHTML = html;
  showSection('section-cartographer');
}

function renderHistorian(d) {
  var rows = (d.precedents||[]).map(function(p) {
    return '<tr><td>' + esc(p.case_description||'') + '</td>'
         + '<td>' + esc(p.what_actually_happened||'') + '</td>'
         + '<td>' + esc(p.key_lesson||'') + '</td></tr>';
  }).join('');

  var html = makeSection('HISTORIAN — HISTORICAL PRECEDENTS',
    '<div class="recommendation-text">' + esc(d.base_rate_insight||'') + '</div>'
    + '<table class="data-table"><thead><tr>'
    + '<th>CASE</th><th>WHAT HAPPENED</th><th>KEY LESSON</th>'
    + '</tr></thead><tbody>' + rows + '</tbody></table>'
    + (d.surprising_finding ? '<div class="plain-text" style="font-style:italic;margin-top:1rem">— ' + esc(d.surprising_finding) + '</div>' : '')
  );
  var el = document.getElementById('section-historian');
  el.innerHTML = html;
  showSection('section-historian');
}

function renderSimulator(d) {
  var horizons = ['0-3 months','3-12 months','1-3 years','3-10 years'];
  var consequences = d.consequences || {};
  var groups = horizons.map(function(h) {
    var items = (consequences[h]||[]).map(function(c) {
      var type = c.type || 'uncertain';
      return '<div class="consequence-item ' + type + '">'
           + '<div class="consequence-desc">' + esc(c.description||'') + '</div>'
           + '<div class="consequence-meta">' + Math.round((c.probability||0)*100) + '% likely · severity ' + (c.severity||'?') + '/10</div>'
           + '</div>';
    }).join('');
    return '<div class="horizon-group"><div class="horizon-label">' + h.toUpperCase() + '</div>' + items + '</div>';
  }).join('');

  var chains = (d.cascade_chains||[]).map(function(c) {
    var parts = c.split('→').map(function(p) { return esc(p.trim()); });
    return '<div class="cascade-chain">' + parts.join('<span class="cascade-arrow">→</span>') + '</div>';
  }).join('');

  var html = makeSection('SIMULATOR — CONSEQUENCE MAP', groups
    + (chains ? '<div class="section-label" style="margin-top:2rem;margin-bottom:1rem">CASCADE CHAINS</div>' + chains : '')
  );
  var el = document.getElementById('section-simulator');
  el.innerHTML = html;
  showSection('section-simulator');
}

function renderAdvocate(d) {
  var assumptions = (d.false_assumptions||[]).map(function(a) {
    return '<tr><td>' + esc(a.assumption||'') + '</td><td style="color:var(--neg-text)">' + esc(a.reality||'') + '</td></tr>';
  }).join('');

  var biases = (d.emotional_biases||[]).map(function(b) {
    return esc(typeof b === 'string' ? b : b.bias || JSON.stringify(b));
  }).join(', ');

  var questions = (d.critical_questions||[]).map(function(q,i) {
    return '<div class="critical-question"><span class="q-number">0' + (i+1) + '</span><span class="q-text">' + esc(q) + '</span></div>';
  }).join('');

  var html = makeSection("DEVIL'S ADVOCATE — BLIND SPOTS",
    '<div class="result-section-inner">'
    + '<table class="data-table"><thead><tr><th>ASSUMPTION</th><th style="color:var(--neg-text)">REALITY</th></tr></thead><tbody>' + assumptions + '</tbody></table>'
    + (biases ? '<div class="plain-text" style="font-style:italic;margin-bottom:1.5rem"><span style="font-family:JetBrains Mono,monospace;font-size:0.7rem;color:var(--text-3)">BIASES &nbsp;</span>' + biases + '</div>' : '')
    + (d.worst_case_scenario ? '<div class="section-label" style="color:var(--neg-text);margin-bottom:0.5rem">WORST CASE</div><div class="plain-text" style="color:var(--neg-text);margin-bottom:1.5rem">' + esc(d.worst_case_scenario) + '</div>' : '')
    + (d.what_they_are_avoiding ? '<div class="uncomfortable-truth">' + esc(d.what_they_are_avoiding) + '</div>' : '')
    + questions
    + '</div>'
  );
  var el = document.getElementById('section-advocate');
  el.innerHTML = html;
  showSection('section-advocate');
}

function renderReframer(d) {
  var alts = (d.alternative_decisions||[]).map(function(a,i) {
    var title = typeof a === 'string' ? a : (a.decision || a.title || JSON.stringify(a));
    var rationale = typeof a === 'object' ? (a.rationale || '') : '';
    return '<div style="padding:1rem 0;border-bottom:1px solid var(--border)">'
         + '<div style="font-weight:500;margin-bottom:0.25rem">' + (i+1) + '. ' + esc(title) + '</div>'
         + (rationale ? '<div style="color:var(--text-2);font-size:0.9rem">' + esc(rationale) + '</div>' : '')
         + '</div>';
  }).join('');

  var html = makeSection('REFRAMER — THE THIRD OPTION',
    '<div class="result-section-inner">'
    + (d.false_dichotomy ? '<div class="plain-text" style="font-style:italic;margin-bottom:2rem">' + esc(d.false_dichotomy) + '</div>' : '')
    + (alts ? '<div class="section-label" style="margin-bottom:0.5rem">ALTERNATIVE PATHS</div>' + alts : '')
    + (d.reframed_question ? '<div class="reframed-question">' + esc(d.reframed_question) + '</div>' : '')
    + (d.minimum_viable_test ? '<div class="mvt-box"><div class="mvt-label">MINIMUM VIABLE TEST</div><div>' + esc(d.minimum_viable_test) + '</div></div>' : '')
    + '</div>'
  );
  var el = document.getElementById('section-reframer');
  el.innerHTML = html;
  showSection('section-reframer');
}

function toggleAccordion(rowEl, bodyEl) {
  var isOpen = rowEl.classList.contains('open');
  document.querySelectorAll('.accordion-row').forEach(function(r) { r.classList.remove('open'); });
  document.querySelectorAll('.accordion-body').forEach(function(b) { b.classList.remove('open'); });
  if (!isOpen) {
    rowEl.classList.add('open');
    bodyEl.classList.add('open');
  }
}

function renderVerdict(d) {
  var rawConf = String(d.confidence_level || '0');
  var match = rawConf.match(/\d+/);
  var confidence = match ? parseInt(match[0]) : 0;
  if (confidence > 100) confidence = Math.round(confidence / 10);

  var verdictHtml = '<div class="verdict-card">'
    + '<div class="recommendation-text">' + esc(d.recommendation||'') + '</div>'
    + '<div class="confidence-bar-container">'
    + '<div class="confidence-label">CONFIDENCE: ' + confidence + '%</div>'
    + '<div class="confidence-track"><div class="confidence-fill" style="width:' + confidence + '%"></div></div>'
    + '</div>'
    + (d.the_one_question ? '<div class="the-one-question"><div class="one-q-label">THE ONE QUESTION TO ANSWER FIRST</div><div class="one-q-text">' + esc(d.the_one_question) + '</div></div>' : '')
    + '</div>';

  var sections = [
    { id: 'section-cartographer', title: 'CARTOGRAPHER — DECISION MAP' },
    { id: 'section-historian', title: 'HISTORIAN — HISTORICAL PRECEDENTS' },
    { id: 'section-simulator', title: 'SIMULATOR — CONSEQUENCE MAP' },
    { id: 'section-advocate', title: 'DEVIL\'S ADVOCATE — BLIND SPOTS' },
    { id: 'section-reframer', title: 'REFRAMER — THE THIRD OPTION' }
  ];

  var accHtml = '';
  sections.forEach(function(s) {
    var sourceEl = document.getElementById(s.id);
    var content = sourceEl.innerHTML;
    sourceEl.innerHTML = '';
    sourceEl.classList.add('hidden');
    
    accHtml += '<div class="accordion-row" onclick="toggleAccordion(this, this.nextElementSibling)">'
             + s.title + '<span class="accordion-icon">+</span></div>'
             + '<div class="accordion-body">' + content + '</div>';
  });

  var html = verdictHtml + accHtml;
  var el = document.getElementById('section-verdict');
  el.innerHTML = html;
  showSection('section-verdict');
  
  document.querySelector('.confidence-fill').style.width = confidence + '%';

  if (d.decision_tree) {
    renderD3Tree(d.decision_tree);
  }
}

function renderD3Tree(treeData) {
  if (!treeData || typeof d3 === 'undefined') return;
  var container = document.getElementById('section-tree');
  container.innerHTML = '<div class="section-label" style="margin-bottom:1rem">CONSEQUENCE MAP</div><div class="section-rule"></div><div id="d3-tree-svg"></div>';
  container.classList.remove('hidden');

  var width = 860;
  var margin = { top: 40, right: 40, bottom: 40, left: 40 };

  var root = d3.hierarchy(treeData);
  var treeLayout = d3.tree().size([width - margin.left - margin.right, 500]);
  treeLayout(root);

  var svg = d3.select('#d3-tree-svg').append('svg')
    .attr('viewBox', '0 0 ' + width + ' 580')
    .style('background', '#111116');

  var g = svg.append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

  g.selectAll('.link').data(root.links()).enter()
    .append('path').attr('class','link')
    .attr('fill','none')
    .attr('stroke','rgba(255,255,255,0.07)')
    .attr('stroke-width',1)
    .attr('d', d3.linkVertical()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; }));

  var colorMap = { positive:'#3d6b52', negative:'#6b3d3d', uncertain:'#3d3d52' };
  var strokeMap = { positive:'#7ec8a0', negative:'#c87e7e', uncertain:'#9898c8' };

  var node = g.selectAll('.node').data(root.descendants()).enter()
    .append('g').attr('class','node')
    .attr('transform', function(d) { return 'translate(' + d.x + ',' + d.y + ')'; })
    .style('opacity',0)
    .transition().delay(function(d,i) { return i * 80; }).duration(400)
    .style('opacity',1);

  g.selectAll('.node').append('circle')
    .attr('r', function(d) { return 6 + ((d.data.probability||0.5) * 16); })
    .attr('fill', function(d) { return colorMap[d.data.type] || '#3d3d52'; })
    .attr('stroke', function(d) { return strokeMap[d.data.type] || '#9898c8'; })
    .attr('stroke-width', 1);

  g.selectAll('.node').append('text')
    .attr('dy', function(d) { return d.children ? -16 : 20; })
    .attr('text-anchor','middle')
    .attr('fill','rgba(140,138,158,0.8)')
    .attr('font-family','JetBrains Mono, monospace')
    .attr('font-size','10')
    .text(function(d) {
      var name = d.data.name || '';
      return name.length > 35 ? name.substring(0,35) + '...' : name;
    });
}

function esc(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

function resetApp() {
  document.getElementById('results-section').classList.add('hidden');
  document.getElementById('new-decision-btn').classList.add('hidden');
  document.getElementById('input-section').classList.remove('hidden');
  document.getElementById('decision-input').value = '';
  document.getElementById('decision-input').style.height = '';
  document.getElementById('divider-line').style.background = 'rgba(255,255,255,0.07)';
  setProgress(0);
  setStatus(null);
  var sections = document.querySelectorAll('.result-section');
  sections.forEach(function(s) {
    s.innerHTML = '';
    s.classList.add('hidden');
  });
}
