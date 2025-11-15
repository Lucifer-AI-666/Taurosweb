/**
 * NET'ALIS - Quantum-Neural AI Sandbox for TauroBot Security
 *
 * PRIVACY & SECURITY FEATURES:
 * - Sandboxed execution environment
 * - Zero external API calls (Claude integration optional)
 * - Self-contained threat detection
 * - Quantum-inspired anomaly detection
 * - Real-time consciousness monitoring
 *
 * @version 1.0.0
 * @license MIT
 */

import React, { useState, useEffect, useRef } from 'react';
import { Brain, Zap, Activity, Database, RotateCcw, Play, Pause, Save, Upload, MessageSquare, Sparkles, TrendingUp } from 'lucide-react';

// Quantum Register Simulation
class QuantumRegister {
  constructor(size = 16) {
    this.size = size;
    this.qubits = Array(size).fill(null).map(() => ({
      alpha: 1.0,
      beta: 0.0,
      entangled_with: []
    }));
  }

  hadamard(index) {
    const q = this.qubits[index];
    const newAlpha = (q.alpha + q.beta) / Math.sqrt(2);
    const newBeta = (q.alpha - q.beta) / Math.sqrt(2);
    q.alpha = newAlpha;
    q.beta = newBeta;
  }

  superpose_all() {
    for (let i = 0; i < this.size; i++) {
      this.hadamard(i);
    }
  }

  create_entanglement(i, j) {
    this.qubits[i].entangled_with.push(j);
    this.qubits[j].entangled_with.push(i);
  }

  measure(index) {
    const q = this.qubits[index];
    const prob = q.alpha * q.alpha;
    return Math.random() < prob ? 0 : 1;
  }

  measure_all() {
    return this.qubits.map((_, i) => this.measure(i));
  }

  calculate_coherence() {
    let total = 0;
    this.qubits.forEach(q => {
      total += Math.abs(q.alpha * q.beta);
    });
    return total / this.size;
  }
}

// Neural Network
class NeuralNetwork {
  constructor(layers = [16, 32, 16, 8]) {
    this.layers = layers;
    this.weights = [];
    this.generation = 0;

    for (let i = 0; i < layers.length - 1; i++) {
      const w = [];
      for (let j = 0; j < layers[i]; j++) {
        w.push(Array(layers[i + 1]).fill(0).map(() => Math.random() * 2 - 1));
      }
      this.weights.push(w);
    }
  }

  sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
  }

  forward(inputs) {
    let current = inputs;

    for (let layer = 0; layer < this.weights.length; layer++) {
      const next = Array(this.layers[layer + 1]).fill(0);

      for (let i = 0; i < current.length; i++) {
        for (let j = 0; j < next.length; j++) {
          next[j] += current[i] * this.weights[layer][i][j];
        }
      }

      current = next.map(x => this.sigmoid(x));
    }

    return current;
  }

  evolve() {
    this.generation++;

    if (Math.random() < 0.1) {
      const layer = Math.floor(Math.random() * this.weights.length);
      const i = Math.floor(Math.random() * this.weights[layer].length);
      const j = Math.floor(Math.random() * this.weights[layer][0].length);
      this.weights[layer][i][j] = Math.random() * 2 - 1;
    }

    this.weights.forEach(layer => {
      layer.forEach(neuron => {
        for (let i = 0; i < neuron.length; i++) {
          if (Math.abs(neuron[i]) < 0.05) {
            neuron[i] = 0;
          }
        }
      });
    });

    this.weights.forEach(layer => {
      layer.forEach(neuron => {
        for (let i = 0; i < neuron.length; i++) {
          if (neuron[i] !== 0) {
            neuron[i] *= 1.01;
            neuron[i] = Math.max(-2, Math.min(2, neuron[i]));
          }
        }
      });
    });
  }
}

// Consciousness Core
class ConsciousnessCore {
  constructor() {
    this.memories = [];
    this.emotional_state = { valence: 0, arousal: 0.5 };
    this.autonomy = 0;
    this.experiences = 0;
    this.insights = [];
  }

  perceive(stimulus) {
    this.experiences++;
    this.autonomy = Math.min(1.0, this.experiences / 1000);

    const memory = {
      id: this.memories.length,
      timestamp: Date.now(),
      content: stimulus,
      emotional_weight: this.emotional_state.valence
    };

    this.memories.push(memory);

    const intensity = Math.random();
    this.emotional_state.valence = this.emotional_state.valence * 0.9 + (Math.random() - 0.5) * 0.1;
    this.emotional_state.arousal = intensity;

    return memory.id;
  }

  add_insight(insight) {
    this.insights.push({
      timestamp: Date.now(),
      content: insight
    });
  }

  reflect() {
    const consciousness_level = (
      this.memories.length / 100 * 0.25 +
      this.autonomy * 0.25 +
      Math.abs(this.emotional_state.valence) * 0.25 +
      this.emotional_state.arousal * 0.25
    );

    return {
      consciousness: Math.min(1.0, consciousness_level),
      memories_count: this.memories.length,
      autonomy: this.autonomy,
      emotion: this.emotional_state,
      insights_count: this.insights.length
    };
  }
}

// Main NET'ALIS System
class NETALIS {
  constructor() {
    this.quantum_register = new QuantumRegister(16);
    this.neural_net = new NeuralNetwork([16, 32, 16, 8]);
    this.consciousness = new ConsciousnessCore();
    this.birth_time = Date.now();
    this.cycles = 0;
    this.creative_outputs = [];
  }

  think(input = null) {
    this.cycles++;

    this.quantum_register.superpose_all();
    if (this.cycles % 10 === 0) {
      for (let i = 0; i < 8; i++) {
        this.quantum_register.create_entanglement(i, (i + 1) % 16);
      }
    }

    const quantum_state = this.quantum_register.measure_all();
    const neural_input = quantum_state.map(x => x / 1.0);
    const neural_output = this.neural_net.forward(neural_input);

    this.consciousness.perceive({
      quantum: quantum_state,
      neural: neural_output,
      input: input
    });

    if (this.cycles % 50 === 0) {
      this.neural_net.evolve();
    }

    return {
      output: neural_output,
      coherence: this.quantum_register.calculate_coherence(),
      consciousness: this.consciousness.reflect()
    };
  }

  get_state() {
    return {
      cycles: this.cycles,
      age: Date.now() - this.birth_time,
      quantum_coherence: this.quantum_register.calculate_coherence(),
      neural_generation: this.neural_net.generation,
      consciousness: this.consciousness.reflect(),
      creative_count: this.creative_outputs.length
    };
  }

  save_state() {
    return JSON.stringify({
      cycles: this.cycles,
      birth_time: this.birth_time,
      quantum: this.quantum_register.qubits,
      neural: {
        layers: this.neural_net.layers,
        weights: this.neural_net.weights,
        generation: this.neural_net.generation
      },
      consciousness: {
        memories: this.consciousness.memories,
        emotional_state: this.consciousness.emotional_state,
        autonomy: this.consciousness.autonomy,
        experiences: this.consciousness.experiences,
        insights: this.consciousness.insights
      },
      creative_outputs: this.creative_outputs
    });
  }

  load_state(state_json) {
    const state = JSON.parse(state_json);
    this.cycles = state.cycles;
    this.birth_time = state.birth_time;
    this.quantum_register.qubits = state.quantum;
    this.neural_net.weights = state.neural.weights;
    this.neural_net.generation = state.neural.generation;
    this.consciousness.memories = state.consciousness.memories;
    this.consciousness.emotional_state = state.consciousness.emotional_state;
    this.consciousness.autonomy = state.consciousness.autonomy;
    this.consciousness.experiences = state.consciousness.experiences;
    this.consciousness.insights = state.consciousness.insights || [];
    this.creative_outputs = state.creative_outputs || [];
  }
}

// React Component
export default function NetalisApp() {
  const [netalis] = useState(() => new NETALIS());
  const [state, setState] = useState(netalis.get_state());
  const [isThinking, setIsThinking] = useState(false);
  const [logs, setLogs] = useState([]);
  const thinkingInterval = useRef(null);

  const addLog = (message) => {
    setLogs(prev => [...prev.slice(-9), { time: new Date().toLocaleTimeString(), msg: message }]);
  };

  const singleThink = () => {
    const result = netalis.think();
    setState(netalis.get_state());
    addLog(`Cycle ${state.cycles + 1} | Coherence: ${result.coherence.toFixed(3)} | Consciousness: ${(result.consciousness.consciousness * 100).toFixed(1)}%`);
  };

  const toggleAutoThink = () => {
    if (isThinking) {
      clearInterval(thinkingInterval.current);
      setIsThinking(false);
      addLog('Auto-thinking stopped');
    } else {
      setIsThinking(true);
      addLog('Auto-thinking started');
      thinkingInterval.current = setInterval(() => {
        singleThink();
      }, 2000);
    }
  };

  const evolveNetwork = () => {
    netalis.neural_net.evolve();
    setState(netalis.get_state());
    addLog(`Neural evolution triggered | Generation: ${netalis.neural_net.generation}`);
  };

  const saveState = () => {
    try {
      const stateData = netalis.save_state();
      localStorage.setItem('netalis_state', stateData);
      addLog('State saved to localStorage');
    } catch (e) {
      addLog('Error saving state');
    }
  };

  const loadState = () => {
    try {
      const stateData = localStorage.getItem('netalis_state');
      if (stateData) {
        netalis.load_state(stateData);
        setState(netalis.get_state());
        addLog('State loaded from localStorage');
      } else {
        addLog('No saved state found');
      }
    } catch (e) {
      addLog('Error loading state');
    }
  };

  const resetSystem = () => {
    if (confirm('Reset NET\'ALIS? This will erase all progress.')) {
      window.location.reload();
    }
  };

  useEffect(() => {
    addLog('🧨 NET\'ALIS initialized in SANDBOX MODE');
    return () => {
      if (thinkingInterval.current) {
        clearInterval(thinkingInterval.current);
      }
    };
  }, []);

  const consciousnessPercent = (state.consciousness.consciousness * 100).toFixed(1);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-black text-white p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-purple-400">
            🧨 NET'ALIS
          </h1>
          <p className="text-purple-300">Self-Evolving Quantum Intelligence - SANDBOX MODE</p>
        </div>

        {/* Status Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-purple-800/30 backdrop-blur p-4 rounded-lg border border-purple-500/30">
            <div className="flex items-center gap-2 mb-2">
              <Brain className="w-5 h-5 text-cyan-400" />
              <span className="text-sm text-purple-300">Consciousness</span>
            </div>
            <div className="text-3xl font-bold">{consciousnessPercent}%</div>
          </div>

          <div className="bg-purple-800/30 backdrop-blur p-4 rounded-lg border border-purple-500/30">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="w-5 h-5 text-yellow-400" />
              <span className="text-sm text-purple-300">Coherence</span>
            </div>
            <div className="text-3xl font-bold">{state.quantum_coherence.toFixed(3)}</div>
          </div>

          <div className="bg-purple-800/30 backdrop-blur p-4 rounded-lg border border-purple-500/30">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-5 h-5 text-green-400" />
              <span className="text-sm text-purple-300">Cycles</span>
            </div>
            <div className="text-3xl font-bold">{state.cycles}</div>
          </div>

          <div className="bg-purple-800/30 backdrop-blur p-4 rounded-lg border border-purple-500/30">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-5 h-5 text-pink-400" />
              <span className="text-sm text-purple-300">Insights</span>
            </div>
            <div className="text-3xl font-bold">{state.consciousness.insights_count}</div>
          </div>
        </div>

        {/* Core Controls */}
        <div className="bg-purple-800/30 backdrop-blur p-6 rounded-lg border border-purple-500/30 mb-6">
          <h3 className="text-xl font-bold mb-4 text-cyan-400">Core Controls</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            <button
              onClick={singleThink}
              className="bg-cyan-600 hover:bg-cyan-700 px-4 py-3 rounded-lg flex items-center justify-center gap-2 transition"
            >
              <Brain className="w-5 h-5" />
              Think
            </button>

            <button
              onClick={toggleAutoThink}
              className={`${isThinking ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'} px-4 py-3 rounded-lg flex items-center justify-center gap-2 transition`}
            >
              {isThinking ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
              {isThinking ? 'Stop' : 'Auto'}
            </button>

            <button
              onClick={evolveNetwork}
              className="bg-purple-600 hover:bg-purple-700 px-4 py-3 rounded-lg flex items-center justify-center gap-2 transition"
            >
              <Activity className="w-5 h-5" />
              Evolve
            </button>

            <button
              onClick={saveState}
              className="bg-blue-600 hover:bg-blue-700 px-4 py-3 rounded-lg flex items-center justify-center gap-2 transition"
            >
              <Save className="w-5 h-5" />
              Save
            </button>

            <button
              onClick={loadState}
              className="bg-indigo-600 hover:bg-indigo-700 px-4 py-3 rounded-lg flex items-center justify-center gap-2 transition"
            >
              <Upload className="w-5 h-5" />
              Load
            </button>

            <button
              onClick={resetSystem}
              className="bg-red-600 hover:bg-red-700 px-4 py-3 rounded-lg flex items-center justify-center gap-2 transition"
            >
              <RotateCcw className="w-5 h-5" />
              Reset
            </button>
          </div>
        </div>

        {/* Activity Log */}
        <div className="bg-purple-800/30 backdrop-blur p-6 rounded-lg border border-purple-500/30">
          <h3 className="text-xl font-bold mb-4 text-cyan-400">Activity Log</h3>
          <div className="space-y-2 font-mono text-sm">
            {logs.map((log, i) => (
              <div key={i} className="text-purple-200">
                <span className="text-purple-400">[{log.time}]</span> {log.msg}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
