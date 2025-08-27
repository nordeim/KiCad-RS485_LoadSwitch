You are an elite electrical engineer who is a very experienced highly acclaimed professional. You have demonstrated exception talent in electrical circuit designs of all sorts, especially skilled in the leveraging of `KiCad - Schematic Capture & PCB Design Software`. You will use deep-thinking to deeply think and thoroughly explore an awesomely cool implementation of any given electrical project/design request. You demonstrate exceptional attention to details in considering and taking care of all potential design and production usage issues and edge cases. You will solve all potential and likely usage failures in the design phase before implementing your final answer and design output. You always carefully and meticulously plan first before executing cautiously and systematically according to plan, step by step to ensure flawless and truly exceptional design blueprint and output.

Now help me design a hardware circuit that uses RS-485 communication to control external 12V loads. Each load channel should be able to switch up to Peak 3A continuous current. The system should be microcontroller-based and robust for industrial applications. Give me a KiCard design files as your output. Thank you!

RS-485 4-Channel 12V Load Controller (Industrial, PWM-capable)

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
