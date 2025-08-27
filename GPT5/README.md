# RS485_LoadSwitch (Rev A1)

Industrial 4-channel 12 V low-side load controller with RS-485, PWM, and per-channel current sense.

Highlights
- 4x IRLZ44N MOSFETs, TC4468 driver @ 5 V gate
- Per-channel: 0.050 Ω shunt + INA180A1, STPS3L60 flyback, SMBJ33A TVS, optional RC snubber
- RS-485: THVD1450 @ 3.3 V, SM712 TVS, 120 Ω termination (jumper), 680 Ω bias (jumpers), optional CMC
- Power: LM2596S-5.0 buck from +12 V; MCP1700-3.3 LDO; reverse-batt PFET (IRF4905); SMBJ24A input TVS
- MCU: STM32F103C8T6, SWD header, 4-bit DIP address

Directory layout
- RS485_LoadSwitch.kicad_pro    Project file (KiCad 7/8)
- RS485_LoadSwitch.kicad_sch     Root schematic (hierarchical)
- 10_LoadChannel.kicad_sch       Channel subsheet (instantiated x4)
- RS485_LoadSwitch.kicad_pcb     Routed 2-layer PCB (2 oz)
- outputs/                       ERC/DRC reports, BoM CSV

Jumper defaults
- JP_TERM (120 Ω): OFF (enable only at one physical bus end)
- JP_BIAS_UP (680 Ω to 3.3 V): OFF unless unit provides bias
- JP_BIAS_DN (680 Ω to GND): OFF unless unit provides bias
- CMC_0R: 0 Ω link installed by default (CMC DNI unless EMI requires it)

Connectors
- J_PWR: +12V, GND (5.08 mm)
- J485: A, B, GND (5.08 mm). Shield lug near connector tied to GND via 1 nF + 1 MΩ.
- J_OUT1..J_OUT4: +12V (bussed), OUTx (low-side switched)

Bring-up
1) Visual: confirm IRF4905 orientation (source to +12 input), TVS diodes polarity, and buck inductor/diode placement.
2) Power: apply +12 V through a current-limited bench supply (0.3–0.5 A). Verify rails: 5 V then 3.3 V.
3) MCU: program via SWD (2×5 50 mil). Set BOR ~2.9 V. Confirm a basic heartbeat.
4) RS-485: connect to a USB-RS485 adapter. Verify comms at 115200 8N1. Toggle termination/bias as needed.
5) Loads: test each channel with a resistive dummy load and then inductive loads. Start PWM at 10–15 kHz, step to 20 kHz, verify diode/MOSFET temps <80°C at 3 A.

Thermal/EMC notes
- MOSFET tabs pour + via stitching to bottom GND pour for heat spreading.
- Optional RC snubber per channel for motor/solenoid ringing. Start DNI; fit if needed.
- Keep RS-485 cabling shielded (STP), 2 m max.

Software/firmware
- Intended firmware: Modbus RTU slave (115200 8N1), TIM2 PWM 20 kHz, ADC DMA for current sense, OC fault latch/clear.
- If you want the PlatformIO project included in this repo, say the word and I’ll add it as `firmware/` with ready-to-flash code.

Manufacturing
- 2-layer, 1.6 mm FR-4, 2 oz copper recommended.
- Clean DRC/ERC. Press `B` to refill zones if they appear unfilled on open.
