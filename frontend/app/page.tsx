'use client';

import { useState, useEffect } from 'react';

export default function Dashboard() {
    const [stats, setStats] = useState({
        activeThreats: 143,
        blockedIps: 892,
        humanRiskScore: 72,
        systemStatus: 'ONLINE'
    });

    const [feed, setFeed] = useState([
        { id: 1, type: 'SSH Brute Force', ip: '192.168.1.5', severity: 'high', time: '10:42 AM' },
        { id: 2, type: 'Phishing Email', ip: '45.33.22.11', severity: 'medium', time: '10:41 AM' },
        { id: 3, type: 'SQL Injection', ip: '103.4.99.1', severity: 'critical', time: '10:40 AM' },
    ]);

    return (
        <main className="min-h-screen grid-bg p-8">
            {/* Header */}
            <header className="flex justify-between items-center mb-10 glass-panel p-6">
                <div>
                    <h1 className="text-3xl font-bold tracking-tighter uppercase glow-text">
                        Cyber Defense <span className="text-[var(--primary)]">Command Center</span>
                    </h1>
                    <p className="text-sm text-gray-400">Organization: ACME Corp (Pro Plan)</p>
                </div>
                <div className="flex gap-4">
                    <div className="text-right">
                        <p className="text-xs text-gray-500 uppercase">System Status</p>
                        <p className="text-[var(--success)] font-mono font-bold">● PROTECTED</p>
                    </div>
                </div>
            </header>

            {/* KPI Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <KpiCard title="Active Threats" value={stats.activeThreats} color="var(--alert-critical)" />
                <KpiCard title="Blocked IPs" value={stats.blockedIps} color="var(--secondary)" />
                <KpiCard title="Human Risk Score" value={`${stats.humanRiskScore}/100`} color="var(--alert-high)" />
                <KpiCard title="Network Flow" value="1.2 GB/s" color="var(--primary)" />
            </div>

            {/* Main Content Split */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Live Attack Map (Placeholder) */}
                <div className="lg:col-span-2 glass-panel p-6 min-h-[400px] flex flex-col">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <span className="w-2 h-2 bg-[var(--primary)] rounded-full animate-pulse"></span>
                        Global Attack Map
                    </h2>
                    <div className="flex-1 bg-black/40 rounded-lg flex items-center justify-center border border-white/5">
                        <p className="text-gray-500 animate-pulse">[ Live GeoIP Visualization Loading... ]</p>
                    </div>
                </div>

                {/* Live Threat Feed */}
                <div className="glass-panel p-6">
                    <h2 className="text-xl font-bold mb-4">Threat Feed</h2>
                    <div className="space-y-3">
                        {feed.map((item) => (
                            <div key={item.id} className="p-3 bg-white/5 rounded border border-white/5 flex justify-between items-center hover:bg-white/10 transition">
                                <div>
                                    <p className="font-bold text-sm text-[var(--foreground)]">{item.type}</p>
                                    <p className="text-xs text-gray-400 font-mono">{item.ip}</p>
                                </div>
                                <div className="text-right">
                                    <Badge severity={item.severity} />
                                    <p className="text-[10px] text-gray-500 mt-1">{item.time}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

            </div>
        </main>
    );
}

function KpiCard({ title, value, color }: { title: string, value: string | number, color: string }) {
    return (
        <div className="glass-panel p-6 border-l-4" style={{ borderLeftColor: color }}>
            <h3 className="text-gray-400 text-sm uppercase tracking-wide">{title}</h3>
            <p className="text-3xl font-bold mt-1" style={{ color: color }}>{value}</p>
        </div>
    );
}

function Badge({ severity }: { severity: string }) {
    const colors: any = {
        critical: 'bg-[var(--alert-critical)] text-white',
        high: 'bg-[var(--alert-high)] text-white',
        medium: 'bg-yellow-500 text-black',
        low: 'bg-blue-500 text-white',
    };
    return (
        <span className={`px-2 py-1 rounded text-[10px] uppercase font-bold ${colors[severity] || 'bg-gray-500'}`}>
            {severity}
        </span>
    );
}
