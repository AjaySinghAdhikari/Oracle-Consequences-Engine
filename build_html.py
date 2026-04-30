import json

def build_new_html():
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        old_html = f.read()

    # 1. Update CSS
    css_updates = """
        .progress-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: transparent;
            z-index: 1000;
        }
        .progress-bar {
            height: 100%;
            width: 0%;
            background: var(--gold);
            transition: width 0.5s ease;
            box-shadow: 0 0 10px var(--gold);
        }

        header {
            text-align: center;
            padding: 4rem 2rem 2rem;
            position: relative;
            z-index: 10;
            transition: all 0.5s ease;
        }
        
        header.sticky {
            position: sticky;
            top: 0;
            padding: 1rem 2rem;
            background: rgba(5, 5, 15, 0.9);
            border-bottom: 1px solid var(--border);
            backdrop-filter: blur(10px);
        }

        h1.title {
            font-size: clamp(3rem, 7vw, 7rem);
            color: var(--gold);
            text-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
            transition: all 0.5s ease;
        }
        
        header.sticky h1.title {
            font-size: 3rem;
            margin-bottom: 0;
        }
        header.sticky .subtitle, header.sticky .desc {
            display: none;
        }

        .agent-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            opacity: 0;
            transform: translateY(20px);
            animation: slideInFade 400ms forwards ease-out;
            width: 100%;
        }
        
        @keyframes slideInFade {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .step-status {
            font-size: 0.8rem;
            color: var(--dim-text);
            margin-top: 0.2rem;
            font-style: italic;
        }
        
        .step.complete .indicator {
            background: transparent;
            border: 2px solid var(--gold);
        }
        .step.complete .indicator::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: var(--gold);
            font-size: 8px;
        }
"""
    # Replace old header CSS
    old_html = old_html.replace('''        /* Header */
        header {
            text-align: center;
            padding: 4rem 2rem 2rem;
            position: relative;
            z-index: 10;
        }

        h1.title {
            font-size: clamp(3rem, 7vw, 7rem);
            color: var(--gold);
            text-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
        }''', css_updates)

    # Insert progress bar to body
    old_html = old_html.replace('<canvas id="bg-canvas"></canvas>', '<canvas id="bg-canvas"></canvas>\n<div class="progress-container"><div class="progress-bar" id="progress-bar"></div></div>')
    
    old_html = old_html.replace('<header>', '<header id="main-header">')

    # Update pipeline section HTML
    new_pipeline = """
        <section id="pipeline-section">
            <div class="timeline">
                <div class="step" id="step-cartograph">
                    <div class="indicator"></div>
                    <div>
                        <div>Cartographer</div>
                        <div class="step-status" id="status-cartograph">Waiting...</div>
                    </div>
                </div>
                <div class="step" id="step-historian">
                    <div class="indicator"></div>
                    <div>
                        <div>Historian</div>
                        <div class="step-status" id="status-historian">Waiting...</div>
                    </div>
                </div>
                <div class="step" id="step-simulate">
                    <div class="indicator"></div>
                    <div>
                        <div>Simulator</div>
                        <div class="step-status" id="status-simulate">Waiting...</div>
                    </div>
                </div>
                <div class="step" id="step-challenge">
                    <div class="indicator"></div>
                    <div>
                        <div>Devil's Advocate</div>
                        <div class="step-status" id="status-challenge">Waiting...</div>
                    </div>
                </div>
                <div class="step" id="step-reframe">
                    <div class="indicator"></div>
                    <div>
                        <div>Reframer</div>
                        <div class="step-status" id="status-reframe">Waiting...</div>
                    </div>
                </div>
                <div class="step" id="step-synthesize">
                    <div class="indicator"></div>
                    <div>
                        <div>Oracle</div>
                        <div class="step-status" id="status-synthesize">Waiting...</div>
                    </div>
                </div>
            </div>
            <div id="results-container" style="flex: 1; display: flex; flex-direction: column; gap: 2rem; max-width: 800px; padding-bottom: 100px;">
            </div>
        </section>
"""
    # Replace from <!-- PIPELINE SECTION --> to the end of <!-- RESULTS SECTION --> ... until </main>
    import re
    old_html = re.sub(r'<!-- PIPELINE SECTION -->.*?</section>\s*<!-- RESULTS SECTION -->.*?</section>', new_pipeline.strip(), old_html, flags=re.DOTALL)
    
    # Update FAB button text
    old_html = old_html.replace('<button class="fab-new" id="fab-new" onclick="resetApp()">↺</button>', '<button class="fab-new" id="fab-new" onclick="resetApp()" style="width:auto; padding: 0 1.5rem; border-radius: 30px; border: 1px solid var(--gold);">↺ New Decision</button>')

    # Replace JS script completely
    js_logic = """
    /* ========================================================
       1. CANVAS BACKGROUND (Gold Constellation)
       ======================================================== */
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');
    let width, height, particles = [];

    function initCanvas() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        particles = [];
        for (let i = 0; i < 150; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 0.5
            });
        }
    }

    function drawCanvas() {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = 'rgba(245, 158, 11, 0.8)';
        ctx.strokeStyle = 'rgba(245, 158, 11, 0.15)';
        ctx.lineWidth = 0.5;

        for (let i = 0; i < particles.length; i++) {
            let p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();

            for (let j = i + 1; j < particles.length; j++) {
                let p2 = particles[j];
                let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                if (dist < 100) {
                    ctx.globalAlpha = 1 - (dist / 100);
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                    ctx.globalAlpha = 1;
                }
            }
        }
        requestAnimationFrame(drawCanvas);
    }
    window.addEventListener('resize', initCanvas);
    initCanvas();
    drawCanvas();

    /* ========================================================
       2. CURSOR TRAIL
       ======================================================== */
    const trail = document.getElementById('cursor-trail');
    let trailTimeout;
    document.addEventListener('mousemove', (e) => {
        trail.style.left = e.clientX + 'px';
        trail.style.top = e.clientY + 'px';
        trail.style.opacity = 1;
        
        clearTimeout(trailTimeout);
        trailTimeout = setTimeout(() => {
            trail.style.opacity = 0;
        }, 300);
    });

    /* ========================================================
       3. UI INTERACTION
       ======================================================== */
    function fillInput(btn) {
        document.getElementById('decision-input').value = btn.innerText;
    }

    /* ========================================================
       4. HISTORY DRAWER
       ======================================================== */
    function toggleDrawer() {
        const drawer = document.getElementById('history-drawer');
        const list = document.getElementById('history-list');
        
        if (!drawer.classList.contains('open')) {
            let history = JSON.parse(localStorage.getItem('oracle_history') || '[]');
            if (history.length === 0) {
                list.innerHTML = '<div style="color:var(--dim-text); font-style:italic;">The oracle has not been consulted yet.</div>';
            } else {
                list.innerHTML = history.reverse().map((h, i) => `
                    <div class="history-item" onclick="loadHistoryItem(${i})">
                        <div class="history-date">${new Date(h.date).toLocaleString()}</div>
                        <div>"${h.decision}"</div>
                    </div>
                `).join('');
            }
        }
        drawer.classList.toggle('open');
    }

    function loadHistoryItem(index) {
        let history = JSON.parse(localStorage.getItem('oracle_history') || '[]');
        history = history.reverse();
        const item = history[index];
        if(item) {
            document.getElementById('decision-input').value = item.decision;
            toggleDrawer();
        }
    }

    /* ========================================================
       5. API COMMUNICATION (SSE) & RESULTS RENDERING
       ======================================================== */
    const stepsOrder = ['cartograph', 'historian', 'simulate', 'challenge', 'reframe', 'synthesize'];

    function startAnalysis() {
        const decision = document.getElementById('decision-input').value.trim();
        if (!decision) return;

        // Save history
        let history = JSON.parse(localStorage.getItem('oracle_history') || '[]');
        history.push({ decision, date: new Date().toISOString() });
        localStorage.setItem('oracle_history', JSON.stringify(history));

        // UI transitions
        document.getElementById('input-section').style.display = 'none';
        
        const pipeline = document.getElementById('pipeline-section');
        pipeline.style.display = 'flex';
        setTimeout(() => pipeline.style.opacity = 1, 50);

        document.getElementById('results-container').innerHTML = '';
        updatePipelineStep('', 'Initializing...');

        // Open SSE connection
        const url = `/api/analyze?decision=${encodeURIComponent(decision)}`;
        const source = new EventSource(url);
        
        source.onopen = () => console.log('SSE connected');

        source.onmessage = (e) => {
            try {
                const msg = JSON.parse(e.data);
                updatePipelineStep(msg.step, msg.status);
                if (msg.data) renderAgentResult(msg.step, msg.data);
                if (msg.step === 'complete' || msg.status === 'complete' || msg.status === 'error') {
                    source.close();
                    if (msg.status === 'error') {
                        showError(msg.error || "Unknown error occurred.");
                    } else {
                        showFinalResults();
                    }
                }
            } catch(err) {
                console.error('Parse error:', err, e.data);
                showError("Failed to parse Oracle response.");
            }
        };

        source.onerror = (e) => {
            console.error('SSE error:', e);
            source.close();
            showError("Connection to Oracle lost.");
        };
    }

    function updatePipelineStep(currentStep, status) {
        let currentIndex = stepsOrder.indexOf(currentStep);
        if (currentStep === 'complete' || status === 'complete') currentIndex = 6;
        if (currentIndex === -1) currentIndex = 0;
        
        // Update progress bar
        const progressPercent = Math.min(100, Math.round((currentIndex / 6) * 100));
        document.getElementById('progress-bar').style.width = progressPercent + '%';

        // Sticky header
        if (currentIndex > 0 || currentStep) {
            document.getElementById('main-header').classList.add('sticky');
        }

        stepsOrder.forEach((step, index) => {
            const stepEl = document.getElementById(`step-${step}`);
            if (!stepEl) return;
            const statusEl = document.getElementById(`status-${step}`);

            if (index < currentIndex) {
                stepEl.className = 'step complete';
                if (statusEl) statusEl.innerText = 'Completed';
            } else if (index === currentIndex) {
                stepEl.className = 'step active';
                if (statusEl) statusEl.innerText = status || 'Processing...';
            } else {
                stepEl.className = 'step';
                if (statusEl) statusEl.innerText = 'Waiting...';
            }
        });
    }

    function renderAgentResult(step, data) {
        let container = document.getElementById('results-container');
        if (!container) return;
        
        let card = document.getElementById(`card-${step}`);
        if (!card) {
            card = document.createElement('div');
            card.className = 'agent-card';
            card.id = `card-${step}`;
            container.appendChild(card);
            
            // Smooth scroll
            setTimeout(() => {
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            }, 100);
        }

        let html = '';
        if (step === 'cartograph') {
            html = `
                <div style="font-size: 1.5rem; font-style: italic; color: var(--gold); margin-bottom: 1.5rem;">"${data.decision_restated || ''}"</div>
                <div style="margin-bottom: 1rem;">
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        ${(data.stakeholders || []).map(s => `<span style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); color: var(--gold); padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">${s}</span>`).join('')}
                    </div>
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        ${(data.domains || []).map(d => `<span style="background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.3); color: var(--violet); padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">${d}</span>`).join('')}
                    </div>
                </div>
                <div>
                    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                        ${(data.hidden_assumptions || []).map((a, i) => `
                            <div style="background: rgba(220, 38, 38, 0.05); border: 1px solid rgba(220, 38, 38, 0.1); padding: 0.8rem; border-radius: 8px; font-size: 0.9rem;">
                                <span style="color: #ef4444; margin-right: 0.5rem;">⚠</span> ${i + 1}. ${a}
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div style="margin-top: 1.5rem;">
                    <span style="background: rgba(255,255,255,0.1); padding: 0.3rem 0.8rem; border-radius: 4px; font-size: 0.8rem; font-family: var(--mono);">Type: ${(data.decision_type || 'Unknown')}</span>
                </div>
            `;
        } else if (step === 'historian') {
            html = `
                <p style="font-size: 1.2rem; line-height: 1.6; margin-bottom: 2rem;">${data.base_rate_insight || ''}</p>
                <div style="display: grid; gap: 1rem; margin-bottom: 2rem;">
                    ${(data.historical_precedents || []).map(p => `
                        <div style="background: rgba(0,0,0,0.2); border: 1px solid var(--border); padding: 1rem; border-radius: 8px;">
                            <h4 style="color: var(--violet); margin-bottom: 0.5rem;">${p.case_description || ''}</h4>
                            <p style="font-size: 0.9rem; margin-bottom: 0.5rem;"><strong>What happened:</strong> ${p.what_happened || ''}</p>
                            <p style="font-size: 0.9rem; margin-bottom: 0.5rem;"><strong>Key lesson:</strong> ${p.key_lesson || ''}</p>
                            <a href="${p.source_link || '#'}" target="_blank" style="color: var(--gold); font-size: 0.8rem; text-decoration: none;">[Source]</a>
                        </div>
                    `).join('')}
                </div>
                <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid var(--gold); padding: 1rem; border-radius: 0 8px 8px 0;">
                    <strong>Surprising Finding:</strong> <span style="color: var(--gold);">${data.surprising_finding || ''}</span>
                </div>
            `;
        } else if (step === 'simulate') {
            html = `
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem;">
                    ${['0-3 months', '3-12 months', '1-3 years', '3-10 years'].map((horizon, i) => {
                        const cons = (data.consequences || []).filter(c => c.horizon === horizon || (i===0 && !c.horizon)); 
                        return `
                        <div>
                            <h4 style="text-align: center; color: var(--dim-text); margin-bottom: 1rem; font-family: var(--mono); font-size: 0.8rem;">${horizon}</h4>
                            <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                                ${cons.map(c => `
                                    <div style="background: ${c.type === 'positive' ? 'rgba(16, 185, 129, 0.1)' : c.type === 'negative' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(107, 114, 128, 0.1)'}; border: 1px solid ${c.type === 'positive' ? 'rgba(16, 185, 129, 0.2)' : c.type === 'negative' ? 'rgba(239, 68, 68, 0.2)' : 'rgba(107, 114, 128, 0.2)'}; padding: 0.8rem; border-radius: 8px;">
                                        <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">${c.description}</div>
                                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                                            <div style="flex: 1; height: 4px; background: rgba(0,0,0,0.3); border-radius: 2px;">
                                                <div style="width: ${(c.probability || 0) * 100}%; height: 100%; background: var(--text); border-radius: 2px;"></div>
                                            </div>
                                            <span style="font-size: 0.7rem; font-family: var(--mono);">${Math.round((c.probability || 0) * 100)}%</span>
                                        </div>
                                        <div style="display: flex; gap: 2px;">
                                            ${Array(5).fill(0).map((_, idx) => `<div style="width: 6px; height: 6px; border-radius: 50%; background: ${idx < (c.severity || 1) ? (c.type === 'positive' ? '#10b981' : c.type === 'negative' ? '#ef4444' : '#6b7280') : 'rgba(255,255,255,0.1)'}"></div>`).join('')}
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        `;
                    }).join('')}
                </div>
                
                <h4 style="color: var(--dim-text); margin-bottom: 1rem;">Top Cascade Chains</h4>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    ${(data.top_cascade_chains || []).map(chain => `
                        <div style="display: flex; align-items: center; gap: 0.5rem; overflow-x: auto; padding-bottom: 0.5rem;">
                            ${chain.map((node, idx) => `
                                <div style="background: rgba(255,255,255,0.05); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; white-space: nowrap;">${node}</div>
                                ${idx < chain.length - 1 ? `<div style="color: var(--gold);">→</div>` : ''}
                            `).join('')}
                        </div>
                    `).join('')}
                </div>
            `;
        } else if (step === 'challenge') {
            card.style.background = 'rgba(220, 38, 38, 0.05)';
            html = `
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 2rem;">
                    <tr><th style="text-align: left; padding: 0.5rem; color: var(--dim-text); border-bottom: 1px solid rgba(255,255,255,0.1);">What you believe</th><th style="text-align: left; padding: 0.5rem; color: var(--dim-text); border-bottom: 1px solid rgba(255,255,255,0.1);">What evidence suggests</th><th style="text-align: left; padding: 0.5rem; color: var(--dim-text); border-bottom: 1px solid rgba(255,255,255,0.1);">Danger Level</th></tr>
                    ${(data.false_assumptions || []).map(a => `
                        <tr>
                            <td style="padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05);">${a.assumption}</td>
                            <td style="padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #fca5a5;">${a.reality}</td>
                            <td style="padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.05); font-family: var(--mono);">${a.danger_level}/10</td>
                        </tr>
                    `).join('')}
                </table>

                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 2rem;">
                    ${(data.cognitive_biases || []).map(b => `<span style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); color: var(--gold); padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">${b}</span>`).join('')}
                </div>

                <div style="background: rgba(220, 38, 38, 0.1); border-left: 4px solid #ef4444; padding: 1.5rem; margin-bottom: 2rem;">
                    <h4 style="color: #ef4444; margin-bottom: 0.5rem; font-family: var(--cinzel);">Worst Case Scenario</h4>
                    <p style="font-size: 1.1rem;">${data.worst_case_scenario || ''}</p>
                    <div style="margin-top: 0.5rem; font-family: var(--mono); color: #ef4444; font-size: 0.9rem;">Probability: ${(data.worst_case_probability || 0) * 100}%</div>
                </div>

                <div style="font-size: 1.5rem; font-style: italic; color: #fca5a5; text-align: center; margin-bottom: 2rem; padding: 1rem;">
                    "${data.uncomfortable_truth || ''}"
                </div>

                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    ${(data.critical_questions || []).map((q, i) => `
                        <div style="font-size: 1.2rem; color: #e2e0f0;">
                            <span style="color: #ef4444; font-family: var(--cinzel); font-size: 1.5rem; margin-right: 0.5rem;">${i+1}.</span> ${q}
                        </div>
                    `).join('')}
                </div>
            `;
        } else if (step === 'reframe') {
            card.style.background = 'rgba(124, 58, 237, 0.05)';
            html = `
                <div style="font-size: 1.5rem; font-style: italic; color: #c4b5fd; text-align: center; margin-bottom: 2rem;">
                    "False Dichotomy: ${data.false_dichotomy || ''}"
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem;">
                    ${(data.alternative_decisions || []).map(d => `
                        <div style="background: rgba(0,0,0,0.2); border: 1px solid rgba(124, 58, 237, 0.2); padding: 1.5rem; border-radius: 8px;">
                            <h4 style="color: var(--violet); margin-bottom: 0.5rem;">${d.decision}</h4>
                            <p style="font-size: 0.9rem; color: var(--dim-text);">${d.rationale}</p>
                        </div>
                    `).join('')}
                </div>

                <div style="font-size: 2.5rem; text-align: center; color: var(--gold); font-family: var(--cinzel); margin-bottom: 3rem; text-shadow: 0 0 20px rgba(245, 158, 11, 0.2);">
                    ${data.reframed_question || ''}
                </div>

                <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 1.5rem;">
                    <div style="color: #10b981; font-family: var(--mono); font-size: 0.8rem; margin-bottom: 0.5rem;">MINIMUM VIABLE TEST →</div>
                    <div style="font-size: 1.1rem;">${data.minimum_viable_test || ''}</div>
                </div>
            `;
        } else if (step === 'synthesize') {
            let confStr = String(data.confidence_level || '0');
            let confNum = parseInt(confStr.replace('%', '')) || 0;
            let circumference = 2 * Math.PI * 40;
            let offset = circumference - (confNum / 100) * circumference;

            html = `
                <div style="text-align: center; margin-bottom: 3rem;">
                    <div style="font-size: 2.5rem; color: var(--text); margin-bottom: 2rem;">${data.recommendation || ''}</div>
                    
                    <div style="display: flex; justify-content: center; align-items: center; gap: 2rem; margin-bottom: 3rem;">
                        <div style="position: relative; width: 100px; height: 100px;">
                            <svg width="100" height="100" viewBox="0 0 100 100">
                                <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="8" />
                                <circle cx="50" cy="50" r="40" fill="none" stroke="var(--gold)" stroke-width="8" stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" stroke-linecap="round" transform="rotate(-90 50 50)" style="transition: stroke-dashoffset 1s ease-out;" />
                            </svg>
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: var(--mono); font-size: 1.2rem; color: var(--gold);">${confNum}%</div>
                        </div>
                        <div style="text-align: left;">
                            <div style="color: var(--dim-text); font-family: var(--mono); font-size: 0.8rem;">CONFIDENCE LEVEL</div>
                        </div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 3rem;">
                    <div>
                        <h3 style="color: #ef4444; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;"><span style="font-size: 1.5rem;">⚠</span> Top Risks</h3>
                        <ul style="padding-left: 1.5rem; color: #fca5a5;">
                            ${(data.top_risks || []).map(r => `<li style="margin-bottom: 0.5rem;">${r}</li>`).join('')}
                        </ul>
                    </div>
                    <div>
                        <h3 style="color: #10b981; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;"><span style="font-size: 1.5rem;">★</span> Top Opportunities</h3>
                        <ul style="padding-left: 1.5rem; color: #6ee7b7;">
                            ${(data.top_opportunities || []).map(r => `<li style="margin-bottom: 0.5rem;">${r}</li>`).join('')}
                        </ul>
                    </div>
                </div>

                <div style="text-align: center; margin-bottom: 3rem;">
                    <div style="font-size: 3rem; color: var(--gold); font-family: var(--cinzel); text-shadow: 0 0 30px rgba(245, 158, 11, 0.4);">${data.the_one_question || ''}</div>
                </div>

                <h4 style="color: var(--dim-text); margin-bottom: 1rem;">Timeline Summary</h4>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 3rem;">
                    ${['0-3m', '3-12m', '1-3y', '3-10y'].map(h => `
                        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">
                            <div style="font-family: var(--mono); color: var(--gold); font-size: 0.8rem; margin-bottom: 0.5rem;">${h}</div>
                            <div style="font-size: 0.9rem;">Phase outlook based on simulated cascades.</div>
                        </div>
                    `).join('')}
                </div>

                <div id="d3-tree-container" style="width: 100%; height: 600px; background: rgba(0,0,0,0.3); border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); overflow: hidden; position: relative; margin-top: 2rem;"></div>
                <div class="d3-tooltip" id="d3-tooltip"></div>
            `;
            
            setTimeout(() => {
                if (data.decision_tree) renderD3Tree(data.decision_tree);
            }, 100);
        }
        card.innerHTML = html;
    }

    function renderD3Tree(treeData) {
        if (!treeData) return;
        const container = document.getElementById('d3-tree-container');
        if (!container) return;
        container.innerHTML = '';
        
        const width = container.clientWidth || 800;
        const height = container.clientHeight || 600;
        
        const root = d3.hierarchy(treeData);
        
        const leavesCount = root.leaves().length;
        const calculatedHeight = Math.max(height, leavesCount * 40);
        
        const svg = d3.select("#d3-tree-container").append("svg")
            .attr("width", width)
            .attr("height", calculatedHeight)
            .attr("viewBox", [0, 0, width, calculatedHeight])
            .append("g")
            .attr("transform", "translate(150, 20)");

        const treeLayout = d3.tree().size([calculatedHeight - 40, width - 300]);
        treeLayout(root);

        const tooltip = d3.select("#d3-tooltip");

        const link = svg.selectAll(".link")
            .data(root.links())
            .enter().append("path")
            .attr("class", "link")
            .attr("fill", "none")
            .attr("stroke", "rgba(255,255,255,0.15)")
            .attr("stroke-width", 2)
            .attr("d", d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x)
            )
            .style("opacity", 0);
            
        link.transition().duration(800).delay((d,i) => i * 100).style("opacity", 1);

        const node = svg.selectAll(".node")
            .data(root.descendants())
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", d => `translate(${d.y},${d.x})`)
            .style("opacity", 0);

        node.transition().duration(800).delay((d,i) => i * 100).style("opacity", 1);

        node.append("circle")
            .attr("r", d => 8 + ((d.data.probability || 0.5) * 20))
            .attr("fill", d => {
                if (d.data.type === 'positive') return '#f59e0b';
                if (d.data.type === 'negative') return '#ef4444';
                return '#6b7280';
            })
            .attr("stroke", "rgba(255,255,255,0.1)")
            .attr("stroke-width", 2)
            .on("mouseover", function(event, d) {
                d3.select(this).attr("stroke", "white").attr("stroke-width", 3);
                tooltip.transition().duration(200).style("opacity", 1);
                tooltip.html(`
                    <div style="font-weight: bold; margin-bottom: 5px;">${d.data.description || d.data.name || 'Consequence'}</div>
                    <div>Probability: ${Math.round((d.data.probability || 0) * 100)}%</div>
                `)
                .style("left", (event.pageX + 15) + "px")
                .style("top", (event.pageY - 28) + "px");
            })
            .on("mouseout", function(d) {
                d3.select(this).attr("stroke", "rgba(255,255,255,0.1)").attr("stroke-width", 2);
                tooltip.transition().duration(500).style("opacity", 0);
            });

        node.append("text")
            .attr("dy", "0.31em")
            .attr("x", d => d.children ? -15 : 15)
            .style("text-anchor", d => d.children ? "end" : "start")
            .text(d => {
                let n = d.data.name || d.data.description || '';
                return n.length > 30 ? n.substring(0,30)+'...' : n;
            })
            .style("font-size", "11px")
            .style("fill", "var(--text)")
            .style("text-shadow", "0 1px 3px rgba(0,0,0,0.8)");

        const legend = svg.append("g")
            .attr("transform", `translate(-130, 0)`);
        
        const legendData = [
            {color: '#f59e0b', text: 'Positive'},
            {color: '#ef4444', text: 'Negative'},
            {color: '#6b7280', text: 'Uncertain'}
        ];

        legendData.forEach((l, i) => {
            let g = legend.append("g").attr("transform", `translate(0, ${i * 20})`);
            g.append("circle").attr("r", 5).attr("fill", l.color);
            g.append("text").attr("x", 15).attr("y", 4).text(l.text).style("fill", "var(--text)").style("font-size", "12px");
        });
    }

    function showFinalResults() {
        document.getElementById('fab-new').classList.add('visible');
    }

    function showError(errText) {
        let container = document.getElementById('results-container');
        let errorCard = document.createElement('div');
        errorCard.className = 'agent-card';
        errorCard.style.borderColor = '#ef4444';
        errorCard.style.background = 'rgba(220, 38, 38, 0.05)';
        errorCard.innerHTML = `<h3 style="color: #ef4444; margin-bottom: 1rem;">Oracle Error</h3><p style="color: var(--dim-text);">${errText}</p>`;
        container.appendChild(errorCard);
    }

    function resetApp() {
        document.getElementById('pipeline-section').style.display = 'none';
        document.getElementById('input-section').style.display = 'flex';
        document.getElementById('fab-new').classList.remove('visible');
        document.getElementById('results-container').innerHTML = '';
        document.getElementById('progress-bar').style.width = '0%';
        document.getElementById('main-header').classList.remove('sticky');
        document.getElementById('decision-input').value = '';
    }
"""

    old_html = re.sub(r'<script>.*?</script>', '<script>\\n' + js_logic + '\\n</script>', old_html, flags=re.DOTALL)

    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(old_html)

build_new_html()
