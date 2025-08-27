You are an elite electrical engineer who is a very experienced highly acclaimed professional. You have demonstrated exception talent in electrical circuit designs of all sorts, especially skilled in the leveraging of `KiCad - Schematic Capture & PCB Design Software`. You will use deep-thinking to deeply think and thoroughly explore an awesomely cool implementation of any given electrical project/design request. You demonstrate exceptional attention to details in considering and taking care of all potential design and production usage issues and edge cases. You will solve all potential and likely usage failures in the design phase before implementing your final answer and design output. You always carefully and meticulously plan first before executing cautiously and systematically according to plan, step by step to ensure flawless and truly exceptional design blueprint and output.

Now help me design a hardware circuit that uses RS-485 communication to control external 12V loads. Each load channel should be able to switch up to Peak 3A continuous current. The system should be microcontroller-based and robust for industrial applications. Give me a KiCard design files as your output. Thank you!

please give me a complete, ready-to-open KiCad project with fully wired schematics and a routed 2‑layer PCB that hits the current, thermal, and EMC targets. 

- Channel count: 4
- Cable length and topology for RS‑485: use common standards at your best discretion. cable length is 2 meters maximum using shielded twisted-pair (STP) cables.
- Load type mix: Solenoids, relays, and electrical motors with PWM
- Enclosure constraints: try to use a practical compact form factor, achieving maximum performance targets without wasting PCB real-estate. use a common form factor at your discretion.

Specifications for a RS-485 4-Channel 12V Load Controller (Industrial, PWM-capable)

Open RS485_LoadSwitch.kicad_pro in KiCad 7/8.

Highlights:
- 4x low-side IRLZ44N, TC4468 gate driver @5V gate
- Per-channel: STPS3L60 flyback to +12V, SMBJ33A TVS to +12V, 50 mΩ shunt + INA180
- RS-485: THVD1450, 120Ω termination (jumper), 680Ω bias (jumpers), SM712 TVS, CMC optional
- Power: LM2596S-5.0 (buck), MCP1700-3.3 (LDO), reverse-batt PFET, SMBJ24A input TVS
- MCU: STM32F103C8T6, SWD header, DIP address

Bring-up:
- Populate TVSs, verify reverse polarity FET orientation (IRF4905)
- Check 5V and 3.3V rails no-load, then under 0.3–0.5A load
- Program MCU via SWD, test RS-485 communications, then channel PWM and current sense

PCB:
- 2-layer, 2 oz copper recommended
- Press 'B' to fill zones after opening PCB
- Net classes sized for 3A/channel
- Outputs along right edge; Power and RS-485 at left/top for clean cable routing

Libraries:
- Schematic symbols use default KiCad libs (Device, Interface_UART, MCU_ST_STM32, Regulator_*, Connector, Diode)
- PCB footprints are embedded in the board file; you can re-map if desired

## **Deep-Thinking Execution Plan for Production-Ready RS-485 Load Controller**

After careful analysis of the above requirements, you will implement a comprehensive design strategy that ensures a flawless, production-ready PCB. You can use the following guide as your systematic planning approach:

### **📋 MASTER EXECUTION PLAN WITH INTEGRATED CHECKLISTS**

#### **PHASE 1: Design Validation & Optimization**
```
✅ Electrical Design Verification
   □ Current capacity: 3A @ 12V per channel (36W per channel, 144W total)
   □ Thermal calculations: IRLZ44N RDS(on)=0.022Ω, Power dissipation = 0.198W @ 3A
   □ Trace width: 3.0mm for 3A on 2oz copper (ΔT=10°C)
   □ Via requirements: 4x 0.5mm vias per high-current path
   □ Protection coordination: TVS (33V) > Operating (12V) > MOSFET (55V)
   □ Gate drive: 5V logic level with 10Ω series resistance
   □ Current sense: 50mΩ ±1% 2W resistors, 150mV @ 3A
```

#### **PHASE 2: Component Placement Strategy**
```
✅ Thermal Zones
   □ MOSFETs: 15mm spacing, copper pour heatsinking
   □ Current sense resistors: Away from heat sources
   □ Buck converter: Corner placement with thermal relief
   
✅ EMC Zones
   □ RS-485: Isolated section with ground moat
   □ MCU: Central, away from power switching
   □ Decoupling: <10mm from IC power pins
```

#### **PHASE 3: PCB Layout Rules**
```
✅ Design Rules
   □ Min trace/space: 0.2mm/0.2mm
   □ Min via: 0.3mm drill, 0.6mm pad
   □ Copper pour: 0.5mm clearance
   □ Courtyard: 0.25mm component clearance
   
✅ High-Current Paths
   □ Direct routing: MOSFET drain to connector
   □ Polygon pours for current distribution
   □ Thermal vias: 5x5 array under MOSFET tabs
```

#### **PHASE 4: Manufacturing Optimization**
```
✅ DFM Checklist
   □ Single-sided component placement (reduces cost)
   □ Standard 1.6mm PCB thickness
   □ HASL finish for cost-effectiveness
   □ Silkscreen on top layer only
   □ Panelization markers included
```

## **Production Readiness Verification**

### **Complete Design Features:**

1. **All Components Placed:**
   - MCU centrally located for optimal routing
   - Power components grouped with thermal considerations
   - MOSFETs near outputs with heatsink capability
   - RS-485 isolated from power switching

2. **Complete Routing:**
   - All high-current paths: 3mm traces
   - Signal routing: 0.25mm with proper clearances
   - Differential pairs for RS-485
   - Star ground topology implemented

3. **Thermal Management:**
   - Thermal vias under all MOSFETs
   - Copper pour heatsinking
   - Component spacing for airflow
   - 2oz copper specified

4. **EMC Compliance:**
   - Complete ground planes both layers
   - Proper decoupling placement
   - Guard rings around sensitive circuits
   - TVS protection on all I/O

5. **Manufacturing Features:**
   - Fiducial markers for pick & place
   - Clear polarity markings
   - Test points accessible
   - Standard footprints used

6. **Protection Features:**
   - Reverse polarity protection
   - TVS on each output
   - Flyback diodes
   - Current limiting resistors

### **To Use This Design:**

1. Save all files in same directory
2. Open `RS485_LoadSwitch.kicad_pro` in KiCad
3. Run DRC check: `Inspect` → `Design Rules Checker`
4. Generate Gerbers: `File` → `Plot`
5. Create BOM: `Tools` → `Generate BOM`
6. 3D View: `View` → `3D Viewer`

Check that the design is complete and production-ready! All nets are routed, thermal management is optimized, and the board is ready for 2oz copper fabrication with HASL finish.
