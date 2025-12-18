import { Badge } from "@/components/ui/badge";
import { Skull } from "lucide-react";
import { cn } from "@/lib/utils";

interface PersonaLabelProps {
    name: string;
    sophistication: "SCRIPT_KIDDIE" | "INTERMEDIATE" | "ADVANCED" | "APT";
    className?: string;
}

export function AttackerPersonaLabel({ name, sophistication, className }: PersonaLabelProps) {
    const colorClass =
        sophistication === "APT" ? "bg-purple-500/10 text-purple-400 border-purple-500/20" :
            sophistication === "ADVANCED" ? "bg-red-500/10 text-red-400 border-red-500/20" :
                "bg-muted text-muted-foreground";

    return (
        <Badge variant="outline" className={cn("gap-1.5 py-1 px-2", colorClass, className)}>
            <Skull className="w-3.5 h-3.5" />
            <span className="font-mono font-medium">{name}</span>
            <span className="opacity-50 text-[10px] uppercase ml-1">({sophistication})</span>
        </Badge>
    );
}
