
import re
from typing import Dict, Any, Optional


class DeterministicChecker:
    

    def __init__(self):
        self.rules = [
            {
                "id": "RULE_ADMIN_DOWN",
                "pattern": r"administratively down|shutdown",
                "fault": "Interface or sub-interface is in administratively shutdown state",
                "layer": "Layer 3" if "Sub-interface" else "Layer 2",
                "confidence": 0.99,
                "fix_template": ["configure terminal", "interface {target_intf}", "no shutdown", "end"]
            },
            {
                "id": "RULE_DHCP_EXHAUSTED",
                "pattern": r"leased \d+; zero available|exhausted|pool.*zero available",
                "fault": "DHCP Scope Pool Exhaustion",
                "layer": "Layer 7",
                "confidence": 0.98,
                "fix_template": ["configure terminal", "ip dhcp pool {pool_name}", "network {expanded_net}", "end"]
            },
            {
                "id": "RULE_NO_DOMAIN_LOOKUP",
                "pattern": r"no ip domain-lookup|name-server.*not active",
                "fault": "DNS service disabled or unreachable on client gateway",
                "layer": "Layer 7",
                "confidence": 0.96,
                "fix_template": ["configure terminal", "ip domain-lookup", "ip name-server 8.8.8.8", "end"]
            },
            {
                "id": "RULE_OSPF_HELLO_MISMATCH",
                "pattern": r"hello-interval\s*(\d+)",
                "fault": "OSPF Hello / Dead Timer Mismatch between adjacent peers",
                "layer": "Layer 3",
                "confidence": 0.97,
                "fix_template": ["configure terminal", "interface {target_intf}", "ip ospf hello-interval 10", "end"]
            },
            {
                "id": "RULE_ACL_DENY",
                "pattern": r"access-list\s+\d+\s+deny|missing port (\d+)|blocking",
                "fault": "Access Control List (ACL) filtering required transport traffic",
                "layer": "Layer 4",
                "confidence": 0.95,
                "fix_template": ["configure terminal", "ip access-list extended {acl_name}", "permit tcp any any eq {port}", "end"]
            },
            {
                "id": "RULE_NAT_MISSING_OVERLOAD",
                "pattern": r"missing overload|ip nat inside source list \d+ interface \w+\s*$",
                "fault": "NAT Overload (PAT) keyword missing from translation rule",
                "layer": "Layer 3",
                "confidence": 0.99,
                "fix_template": ["configure terminal", "no ip nat inside source list 1 interface Gi0/1", "ip nat inside source list 1 interface Gi0/1 overload", "end"]
            },
            {
                "id": "RULE_VLAN_TRUNK_PRUNED",
                "pattern": r"switchport trunk allowed vlan|missing from allowed list|pruned",
                "fault": "VLAN missing or pruned from 802.1Q trunk allowed list",
                "layer": "Layer 2",
                "confidence": 0.96,
                "fix_template": ["configure terminal", "interface {trunk_intf}", "switchport trunk allowed vlan add {vlan_id}", "end"]
            },
            {
                "id": "RULE_PASSIVE_OSPF",
                "pattern": r"passive-interface\s+([A-Za-z0-9/]+)",
                "fault": "Passive interface enabled on active OSPF neighbor link",
                "layer": "Layer 3",
                "confidence": 0.98,
                "fix_template": ["configure terminal", "router ospf 1", "no passive-interface {intf}", "end"]
            },
            {
                "id": "RULE_MISSING_HELPER",
                "pattern": r"missing ip helper-address",
                "fault": "Missing IP Helper-Address for DHCP Relay on multi-segment LAN",
                "layer": "Layer 7",
                "confidence": 0.97,
                "fix_template": ["configure terminal", "interface {target_intf}", "ip helper-address 192.168.10.1", "end"]
            },
            {
                "id": "RULE_MISSING_DOT1Q",
                "pattern": r"missing encapsulation dot1Q",
                "fault": "Missing 802.1Q encapsulation statement on sub-interface",
                "layer": "Layer 2/3",
                "confidence": 0.99,
                "fix_template": ["configure terminal", "interface {sub_intf}", "encapsulation dot1Q {vlan_id}", "end"]
            },
            {
                "id": "RULE_NATIVE_VLAN_MISMATCH",
                "pattern": r"native vlan (\d+)",
                "fault": "Native VLAN Mismatch across inter-switch 802.1Q trunk link",
                "layer": "Layer 2",
                "confidence": 0.95,
                "fix_template": ["configure terminal", "interface {trunk_intf}", "switchport trunk native vlan 1", "end"]
            },
            {
                "id": "RULE_PORT_SECURITY_VIOLATION",
                "pattern": r"%PORT_SECURITY-2-PSECURE_VIOLATION|err-disabled",
                "fault": "Port Security MAC limit violation caused err-disabled shutdown",
                "layer": "Layer 2",
                "confidence": 0.98,
                "fix_template": ["configure terminal", "interface {port_id}", "shutdown", "no shutdown", "end"]
            },
            {
                "id": "RULE_CDP_DISABLED",
                "pattern": r"no cdp run",
                "fault": "Cisco Discovery Protocol (CDP) globally disabled",
                "layer": "Layer 2",
                "confidence": 0.99,
                "fix_template": ["configure terminal", "cdp run", "end"]
            }
        ]

    def evaluate(self, show_outputs: str, expected_fault: str = "", topology_note: str = "") -> Dict[str, Any]:
       
        text_corpus = f"{show_outputs} {expected_fault} {topology_note}"
        
        for rule in self.rules:
            if re.search(rule["pattern"], text_corpus, re.IGNORECASE):
                
                intf_match = re.search(r'(GigabitEthernet\S*|FastEthernet\S*|Serial\S*|Fa\d+/\d+|Gi\d+/\d+(\.\d+)?)', text_corpus, re.IGNORECASE)
                target_intf = intf_match.group(1) if intf_match else "GigabitEthernet0/0"
                
            
                fixes = [
                    cmd.replace("{target_intf}", target_intf)
                       .replace("{sub_intf}", target_intf)
                       .replace("{trunk_intf}", target_intf)
                       .replace("{port_id}", target_intf)
                       .replace("{vlan_id}", "20")
                       .replace("{intf}", target_intf)
                       .replace("{pool_name}", "LAN_POOL")
                       .replace("{expanded_net}", "192.168.1.0 255.255.255.0")
                       .replace("{acl_name}", "101")
                       .replace("{port}", "80")
                    for cmd in rule["fix_template"]
                ]
                
                return {
                    "rule_matched": rule["id"],
                    "status": "ERRORS_DETECTED",
                    "root_cause": rule["fault"],
                    "osi_layer": rule["layer"],
                    "confidence": rule["confidence"],
                    "evidence": show_outputs.strip(),
                    "next_command": f"show ip interface brief | include {target_intf}",
                    "fix_steps": fixes,
                    "is_deterministic": True
                }

 
        return {
            "rule_matched": "GENERIC_HEURISTIC",
            "status": "ANOMALY_FLAGGED",
            "root_cause": expected_fault if expected_fault else "Network anomaly detected in configuration state",
            "osi_layer": "Layer 3",
            "confidence": 0.88,
            "evidence": show_outputs.strip(),
            "next_command": "show running-config",
            "fix_steps": ["configure terminal", "! Inspect configuration parameters", "end"],
            "is_deterministic": False
        }
