import { Monitor, Smartphone, Globe, Clock } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface Device {
    id: string;
    name: string; // "Chrome on Windows"
    type: "DESKTOP" | "MOBILE";
    ip: string;
    location: string;
    lastSeen: string;
    isCurrent: boolean;
    status: "TRUSTED" | "NEW" | "SUSPICIOUS";
}

export function DeviceHistoryList() {
    // Mock Data (Module B)
    const devices: Device[] = [
        { id: "1", name: "Chrome on Windows", type: "DESKTOP", ip: "192.168.1.10", location: "New York, US", lastSeen: "Now", isCurrent: true, status: "TRUSTED" },
        { id: "2", name: "Safari on iPhone", type: "MOBILE", ip: "10.0.0.5", location: "New York, US", lastSeen: "2 hours ago", isCurrent: false, status: "TRUSTED" },
        { id: "3", name: "Firefox on Linux", type: "DESKTOP", ip: "45.33.22.11", location: "Unknown Proxy", lastSeen: "1 day ago", isCurrent: false, status: "SUSPICIOUS" },
    ];

    return (
        <div className="space-y-4">
            {devices.map((device) => (
                <div key={device.id} className="flex items-center justify-between p-4 border rounded-lg bg-card hover:bg-muted/50 transition-colors">
                    <div className="flex items-center gap-4">
                        <div className="p-2 bg-muted rounded-full">
                            {device.type === "DESKTOP" ? <Monitor className="w-5 h-5" /> : <Smartphone className="w-5 h-5" />}
                        </div>
                        <div>
                            <div className="flex items-center gap-2">
                                <span className="font-medium">{device.name}</span>
                                {device.isCurrent && <Badge variant="secondary" className="text-xs h-5">Current</Badge>}
                                {device.status === "SUSPICIOUS" && <Badge variant="destructive" className="text-xs h-5">Suspicious</Badge>}
                                {device.status === "NEW" && <Badge className="bg-blue-500 hover:bg-blue-600 text-xs h-5">New</Badge>}
                            </div>
                            <div className="flex items-center gap-3 text-sm text-muted-foreground mt-1">
                                <span className="flex items-center gap-1"><Globe className="w-3 h-3" /> {device.ip} ({device.location})</span>
                                <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {device.lastSeen}</span>
                            </div>
                        </div>
                    </div>
                    <div className="text-right">
                        {/* Actions could go here (e.g. Revoke) */}
                    </div>
                </div>
            ))}
        </div>
    );
}
