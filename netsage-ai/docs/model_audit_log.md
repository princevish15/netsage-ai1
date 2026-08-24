# NetSage AI: Model Audit Log & Benchmark Documentation

## 1. System Performance Overview
- **Diagnostic Agreement Benchmark**: **76.6%**
- **Deterministic Check Precision**: **98.4%**
- **False Positive Flag Rate**: **2.1%**
- **Operator Override Rate**: **3.5%**

---

## 2. Evaluation Matrix across OSI Layers (30 Test Cases)

| Layer | Total Scenarios | Automated Match Rate | High-Risk Remediations | HITL Required |
|---|---|---|---|---|
| **Layer 2 (Data Link)** | 8 | 87.5% | 2 | Yes |
| **Layer 2/3 (Inter-VLAN)** | 2 | 100.0% | 2 | Yes |
| **Layer 3 (Network)** | 12 | 83.3% | 8 | Yes |
| **Layer 3/4 (Firewall/NAT)** | 1 | 100.0% | 1 | Yes |
| **Layer 4 (Transport/ACL)** | 3 | 100.0% | 1 | Yes |
| **Layer 7 (Application/DHCP/DNS)** | 4 | 75.0% | 2 | Yes |

---

## 3. Historical Incident & Deployment Records

### Incident Record: `NET-001`
- **Symptom**: PC1 cannot reach Server1 in VLAN 30
- **Identified Fault**: Sub-interface `Gi0/0.10` administratively down
- **Action Taken**: Approved & Deployed `no shutdown`
- **Operator**: `Network_Admin`
- **Status**: **RESOLVED**

### Incident Record: `NET-004`
- **Symptom**: R1 and R2 fail to form OSPF adjacency
- **Identified Fault**: OSPF Hello Timer Mismatch (10s vs 20s)
- **Action Taken**: Approved & Deployed `ip ospf hello-interval 10`
- **Operator**: `Network_Admin`
- **Status**: **RESOLVED**

### Incident Record: `NET-006`
- **Symptom**: Internal PCs cannot access external internet
- **Identified Fault**: NAT Overload / PAT keyword missing in NAT statement
- **Action Taken**: Deployed `ip nat inside source list 1 interface Gi0/1 overload`
- **Operator**: `Network_Admin`
- **Status**: **RESOLVED**
