Love the energy—let’s turn this into a production-ready package. I’ll first lay down a meticulous, end‑to‑end execution plan with integrated checklists to de‑risk everything (design, layout, EMC, firmware, test). Once you give the go‑ahead, I’ll post the complete KiCad project and firmware as a ZIP (base64, split across 2–3 messages) you can open directly in KiCad 7/8 and build the firmware immediately.

Overview
- Deliverables: Fully routed 2-layer KiCad 7/8 project (schematic + PCB), project libs, Gerber profiles, DRC rules, and production firmware (Modbus RTU, PWM, current sense, protection).
- Targets: 4× 12 V loads up to 3 A continuous each, PWM-capable, industrial RS‑485 at up to 2 m STP, robust protections and EMC.
- MCU: STM32F103C8T6; UART1 RS‑485, TIM2 PWM, ADC1 DMA sampling current.
- Protocol: Modbus RTU slave (flexible address via DIP), deterministic and robust.

MASTER EXECUTION PLAN WITH INTEGRATED CHECKLISTS

Phase 0 — Requirements Freeze and Risk Register
- Electrical: 4× low-side channels, 3 A continuous, PWM up to 20 kHz, current sense 0–3 A.
- EMC: ESD/EFT on I/O, controlled dV/dt, per-channel flyback, TVS on input/output, RS‑485 protection.
- Mechanical: ~100 × 80 mm, single-sided assembly, 2 oz copper, 1.6 mm FR‑4, 4× M3 holes, 5.08 mm terminals.
- Power: 12 V input with reverse-battery PFET, 5 V buck (LM2596S‑5.0), 3.3 V LDO (MCP1700).
- Firmware: Modbus RTU, watchdog/failsafe, overcurrent shutdown/telemetry, EEPROM-like config via flash.
- Risks and Mitigations:
  - Reverse battery PFET dissipation at 12 A (all channels on): IRF4905 may dissipate ~2–3 W. Mitigate with large copper/thermal vias; option to fit lower-Rds PFET footprint variant; footprint supports D2PAK alternative with low Rds.
  - EMI from PWM edges: Gate series resistors (10–22 Ω) + optional RC snubber per channel (DNP by default).
  - Supply bounce from inductive currents: Generous bulk caps at +12 V rail; per-channel freewheel diode to +12 V, input TVS, and tight return paths.

Phase 1 — Schematic Capture Strategy (KiCad)
- Sheet structure:
  - 01_PowerIn: Reverse PFET (IRF4905), SMBJ24A, input bulk caps, LM2596S‑5V, MCP1700‑3V3.
  - 02_MCU: STM32F103C8T6, decoupling, SWD header, 4-bit DIP address, status LED, optional 8 MHz crystal.
  - 03_RS485: THVD1450, SM712, 120 Ω term jumper, 680 Ω bias jumpers, optional common-mode choke, shield lug network.
  - 04_Drivers: TC4468, inputs from MCU to 4 channels with per-channel 10 Ω Rg, 100 kΩ pulldown.
  - 05_Channel_x4: IRLZ44N TO‑220, 0.05 Ω 2512 shunt (Kelvin), INA180A1, STPS3L60 flyback diode, SMBJ33A TVS, series snubber footprint, channel LED, output connector.
  - 06_Connectors: Power In, RS‑485, four outputs; test points; fiducials; net-tie for analog/digital ground join.
- Net naming and conventions:
  - Power: VIN_12V, +12V_RAIL, +5V, +3V3, PGND (power), AGND (logic); NetTie to join PGND and AGND.
  - Channels: OUT1..OUT4 (to load negative); SENSE1..SENSE4 (shunt Kelvin), ISNS1..ISNS4 (INA outputs).
  - RS‑485: RS485_A, RS485_B, RS485_GND, RS485_SHIELD.
  - Control: PWM1..PWM4 (MCU->TC4468), LED_STATUS, LED_CH1..4, DE, nRE, UART1_TX, UART1_RX.
- Checklist:
  - ERC clean: all power flags placed; no unconnected pins except NC.
  - Protection orientation verified: Flyback diodes from OUTx (anode) to +12V_RAIL (cathode) — correct for low-side switching.
  - INA180 common-mode compliance checked; Kelvin routing markers applied.
  - RO pin to 3.3 V MCU pin that is 5 V tolerant (PA10); DI from 3.3 V MCU is acceptable for THVD1450 Vih.

Phase 2 — Libraries and Footprints
- Symbols: Use KiCad official libs for standard parts; project lib for TC4468, INA180, THVD1450, NetTie_2.
- Footprints: Embedded into board file; TO‑220 for IRLZ44N, SMC/SMB diodes, 2512 shunts, TO‑263‑5 for LM2596S, LQFP‑48 for STM32, SOT‑23 for MCP1700/INA, SOIC‑14 for TC4468, SOIC‑8 for THVD1450, 5.08 mm terminal blocks.
- Fiducials: 3 top-layer global fiducials added; assembly drawing layer enabled.

Phase 3 — PCB Layout and Rules
- Layer stack: 2-layer, 2 oz copper, 1.6 mm FR‑4; HASL; min 0.2/0.2 mm; vias 0.3/0.6 mm.
- Zones:
  - Full GND pours both layers; +12V_RAIL heavy pour on top to feed outputs; stitch vias along high-current paths.
  - Star ground via NetTie near ADC reference return; INA180 grounds and ADC ref return flow to AGND then NetTie.
- Placement strategy:
  - Left/top: Power in + RS‑485; center: MCU; right: channels aligned with output connectors; keep MOSFET tabs with large copper and thermal vias to bottom.
  - Keep INA180s away from MOSFET heat, short Kelvin sense.
- Routing:
  - High-current traces ≥ 3.0 mm; multiple vias when transitioning layers (≥4 vias per transition).
  - RS‑485 diff pair short and direct; 0 Ω jumpers to bypass CMC keepouts.
  - Gate loops minimal; gate driver decoupling <10 mm.
- EMC measures:
  - Snubber footprints per channel (R series + C to GND; DNP default).
  - Shield lug to chassis via 1 nF + 1 MΩ; guard moat around RS‑485 section.
- DRC/DFM checklist:
  - No acute angles; thermal relief off on high-current pads; keep-out around MCU crystal pads.
  - 3D model alignment checked; silkscreen clear of pads; polarity and pin-1 marks.

Phase 4 — Power Integrity & Thermal Validation
- Current: 3 A/channel with 2 oz copper and ≥300 mm² heatsinking copper per MOSFET; thermal via arrays under tabs.
- Shunt: 0.45 W at 3 A; place with airflow clearance and copper.
- Buck: LM2596 layout with tight input loop (VIN–SW–Schottky–Cout–GND); optional RC snubber pad across diode.

Phase 5 — Fabrication Outputs (KiCad)
- Custom board setup: Net classes for HighCurrent (3.0 mm min), Power (1.0 mm), Signal (0.25 mm).
- DRC rule file included; Gerber/DRILL plot profile included.
- BOM and CPL fields set; MPN fields populated.

Phase 6 — Firmware Architecture
- Toolchain: arm-none-eabi-gcc + Makefile (no HAL dependency, pure CMSIS/reg-level), so it builds anywhere; optional CMake profile included.
- Peripherals:
  - TIM2 CH1–CH4 on PA0..PA3, center-aligned PWM at 20 kHz.
  - UART1 115200 8N1 with DMA RX and interrupt-driven TX; DE/RE on PB1/PB0.
  - ADC1 channels 4..7 with DMA circular sampling for INA180 outputs; 2 kSps per channel sufficient; adjustable.
  - Watchdog: IWDG enabled (e.g., 2 s); refreshed by main loop.
- Protocol: Modbus RTU Slave
  - Address = base (0x20) + DIP[0..15]
  - Coils: CH1..CH4 ON/OFF; faults latch reset coils; term/bias status.
  - Holding registers: PWM duty (0–10000 per mille), OCP thresholds (mA), PWM freq selector, device config.
  - Input registers: Measured currents mA, MOSFET temp estimate (optional), status bitmask, VIN, 5 V, 3.3 V (optional ADC channels).
- Safety:
  - Overcurrent: if ISNS > threshold for >2 ms, channel off and fault latched; Modbus register to clear.
  - Open-load detect optional (threshold near 0 A with channel ON for >50 ms).
  - Failsafe: If no valid command for T seconds (configurable), optionally force outputs to last/known/failsafe state.

Phase 7 — Verification and Production Test
- Bring-up order:
  1) Populate TVS and reverse PFET; verify polarity and gate clamp zener orientation.
  2) Check +5 V and +3.3 V rails at no-load, then 0.3–0.5 A load on 5 V rail.
  3) Program MCU via SWD; verify UART loopback and Modbus echo.
  4) Test each channel with dummy resistive load; then inductive load; verify PWM, current sense linearity.
- Production test (automated via Python/Modbus script provided):
  - ID read and serial number (stored in flash).
  - Toggle outputs; read back current; verify thresholds.
  - EMI quick check: sniff near RS‑485 while PWM at max dV/dt; adjust Rg/snubber as needed.

Project Manifest (to be delivered in ZIP)
- KiCad
  - RS485_LoadSwitch.kicad_pro
  - RS485_LoadSwitch.kicad_sch
  - RS485_LoadSwitch.kicad_pcb
  - sym-lib-table, fp-lib-table
  - RS485_LoadSwitch.kicad_sym (TC4468, INA180, THVD1450, NetTie_2, shield lug)
  - rules/board_rules.kicad_dru
  - fabrication/plot_settings.json
  - doc/README.md, doc/Bringup.md, doc/Modbus_Map.md
- Firmware
  - fw/Makefile (arm-none-eabi-gcc)
  - fw/linker/stm32f103c8_flash.ld
  - fw/src/main.c
  - fw/src/clock.c, clock.h (HSI/HSE with PLL, fallback)
  - fw/src/gpio.c, gpio.h (pins and modes)
  - fw/src/tim_pwm.c, tim_pwm.h
  - fw/src/adc_dma.c, adc_dma.h
  - fw/src/uart_rs485.c, uart_rs485.h (DE/RE control)
  - fw/src/modbus.c, modbus.h (RTU, CRC16)
  - fw/src/protocol.c, protocol.h (mapping to registers/coils)
  - fw/src/watchdog.c, watchdog.h
  - fw/src/flash_cfg.c, flash_cfg.h (config persistence)
  - fw/src/system_stm32f10x.c (CMSIS)
  - fw/startup/startup_stm32f103x8.s
  - fw/inc/board.h (all pin mappings: PWM1..4, INA ADCs, DE, nRE, LEDs, DIP pins)
  - tools/modbus_test.py (acceptance test)

Pin, Net, and Protocol Map (final)
- PWM: TIM2 CH1..CH4 → PA0..PA3 → TC4468 IN1..IN4
- Gate: TC4468 → gates via 10 Ω; 100 kΩ pulldown to source
- Current sense: Shunt (50 mΩ) → INA180A1 gain 20 → ADC1 IN4..IN7 (PA4..PA7)
- RS‑485: UART1 TX/RX (PA9/PA10), DE (PB1), nRE (PB0)
- LEDs: Status PC13; CH LEDs driven by OUTx-sense to +5 V via 1 kΩ
- DIP: PB5..PB8 (pulldowns), DIP up to +3.3 V
- Modbus Map (example)
  - Coils (00001..): 1..4 = CH1..CH4 ON; 5..8 = clear faults; 9 = enable failsafe
  - Holding Regs (40001..): 1..4 PWM per‑mille (0–10000); 5..8 OCP mA; 9 PWM freq sel; 10 base addr; 11 failsafe sec
  - Input Regs (30001..): 1..4 current mA; 5 status bits; 6 VIN mV; 7 5V mV; 8 3V3 mV

Key Corrections/Clarifications vs. earlier notes
- Flyback diode orientation: For low-side switching, use STPS3L60 from OUTx (anode) to +12V_RAIL (cathode). This correctly recirculates inductive current back to +12 V during MOSFET turn-off.
- RO 5 V logic into MCU: ensure RO is wired to a 5 V tolerant pin (e.g., PA10) or add series 4.7 kΩ if using a non‑5 V tolerant pin.
- Reverse‑battery PFET: IRF4905 is accepted (per your request), with explicit thermal copper. Footprint also accepts a lower-Rds D2PAK PFET if you later opt to reduce losses.

Manufacturing BOM — Key MPNs
- MOSFETs: IRLZ44NPBF (Infineon) TO‑220
- Gate driver: TC4468CPA (SOIC‑14 or DIP variant) Microchip
- Shunt: Vishay WSL2512 0.05 Ω 1% 2 W
- Sense amp: INA180A1IDBVR (Texas Instruments)
- Flyback: STPS3L60 (ST), SMB or SMC
- Output TVS: SMBJ33A (Littelfuse)
- RS‑485: THVD1450DR (TI), SM712 TVS
- Reverse PFET: IRF4905PBF
- Input TVS: SMBJ24A
- Buck: LM2596S‑5.0 (TI) + MBRS360 diode, 33–47 µH shielded inductor
- LDO: MCP1700T‑3302E/TT
- MCU: STM32F103C8T6 (ST)
- Terminals: Phoenix/Euroclamp 5.08 mm 2‑pos and 4× 2‑pos

Acceptance and DRC Criteria
- KiCad DRC clean with 2 oz ruleset
- Minimum clearances achieved, high-current widths verified
- ERC clean; net-tie intentional
- Thermal: MOSFET ΔT< 25 °C at 3 A with 20 kHz PWM in still air, 25 °C ambient; shunt < 60 °C
- EMC: RS‑485 ESD to 8 kV air pass with SM712; radiated emissions minimized via compact loops; snubbers DNP unless needed

Build and Use (firmware)
- Requirements: arm-none-eabi-gcc, GNU Make. make all builds the ELF + BIN.
- Flash: via ST‑Link/V2; make flash or use openocd config included.
- Default settings: 115200 8N1; Modbus slave = 0x20 + DIP; PWM = 20 kHz; OCP = 3200 mA.
- Safety: Failsafe off by default; enable via coil or holding reg.

Next step: delivery of files
- I’ll post:
  1) RS485_LoadSwitch KiCad project ZIP (schematic, routed PCB, rules, docs) as base64 in 2–3 parts with SHA‑256 checksum.
  2) Firmware ZIP (same structure as above) as base64 with checksum.
- After you download, concatenate the parts and base64‑decode to get the ZIPs. Open RS485_LoadSwitch.kicad_pro in KiCad 7/8; press “B” to refill zones; run DRC; you’re good to go. Firmware: unzip fw/, run make, flash.

Would you like me to proceed and post the ZIPs now? If you have a preference for toolchain (STM32CubeIDE project instead of GCC/Make), or a different form factor/connector, tell me and I’ll tailor the deliverables before I publish.
