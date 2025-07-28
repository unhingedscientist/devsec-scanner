
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass, field
import time
from ..utils.logger import get_logger, log_performance

@dataclass
class Vulnerability:
    title: str
    description: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    file_path: str
    line_number: int = None
    category: str = None
    cwe_id: str = None
    fix_suggestion: str = None

class BaseScanner(ABC):
    def __init__(self, config):
        self.config = config
        self.vulnerabilities: List[Vulnerability] = []
        self.logger = get_logger(self.__class__.__name__, verbose=getattr(config, 'VERBOSE', False), json_mode=(getattr(config, 'OUTPUT_FORMAT', 'console') == 'json'))

    @abstractmethod
    def scan(self, target: str) -> List[Vulnerability]:
        """Scan target and return vulnerabilities"""
        pass

    @abstractmethod
    def is_supported_target(self, target: str) -> bool:
        """Check if target is supported by this scanner"""
        pass

    def add_vulnerability(self, vuln: Vulnerability):
        """Add vulnerability to results"""
        self.vulnerabilities.append(vuln)

    def run_scan(self, target: str) -> List[Vulnerability]:
        start_time = time.time()
        try:
            self.logger.info(f"Starting scan on: {target}")
            vulns = self.scan(target)
            self.logger.info(f"Scan complete. Found {len(vulns)} vulnerabilities.")
            return vulns
        except Exception as e:
            self.logger.error(f"Scan failed: {e}", exc_info=getattr(self.config, 'VERBOSE', False))
            return []
        finally:
            log_performance(self.logger, f"Scan ({self.__class__.__name__})", start_time)
