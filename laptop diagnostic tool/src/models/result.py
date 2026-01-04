from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class DiagnosticResult:
    name: str
    status: str
    message: str
    details: Optional[Dict[str, Any]] = field(default_factory=dict)
    severity: str = "INFO"
    confidence: str = "medium"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())