import { Badge } from "@/components/ui/badge";
import { ShieldAlert, ShieldCheck, ShieldQuestion } from "lucide-react";

interface RiskBadgeProps {
    score: number;
}

export function RiskBadge({ score }: RiskBadgeProps) {
    if (score >= 80) {
        return (
            <Badge variant="destructive" className="gap-1">
                <ShieldAlert className="w-3 h-3" />
                High Risk ({score})
            </Badge>
        );
    }
    if (score >= 50) {
        return (
            <Badge variant="secondary" className="gap-1 bg-yellow-500/15 text-yellow-600 hover:bg-yellow-500/25 border-yellow-500/50">
                <ShieldQuestion className="w-3 h-3" />
                Medium Risk ({score})
            </Badge>
        );
    }
    return (
        <Badge variant="outline" className="gap-1 text-green-600 border-green-600/50">
            <ShieldCheck className="w-3 h-3" />
            Safe ({score})
        </Badge>
    );
}

interface ThreatBadgeProps {
    type: string; // e.g., "Botnet", "Tor Node"
    confidence?: number;
}

export function ThreatBadge({ type, confidence }: ThreatBadgeProps) {
    return (
        <Badge variant="destructive" className="animate-pulse">
            THR: {type} {confidence ? `(${confidence}%)` : ''}
        </Badge>
    )
}
