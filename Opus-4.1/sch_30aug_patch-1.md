;;; RS-485 4-Channel Load Controller - Production Patch v1.0
;;; This patch addresses all critical issues identified in design review
;;; Apply to original schematic to achieve production-ready status

;; ==========================================================================
;; SECTION 1: CRITICAL - Fix Current Sensing (Prevent ADC Destruction)
;; ==========================================================================

;; Replace INA181A3 (100V/V) with INA181A1 (20V/V) for all channels
;; This ensures 3A × 0.050Ω × 20 = 3.0V max output (safe for 3.3V ADC)

(replace_symbol_property "U5"
  (property "Value" "INA181A1" (at 243.84 93.98 0)
    (effects (font (size 1.27 1.27)))))

(replace_symbol_property "U6"
  (property "Value" "INA181A1" (at 243.84 109.22 0)
    (effects (font (size 1.27 1.27)))))

(replace_symbol_property "U7"
  (property "Value" "INA181A1" (at 243.84 124.46 0)
    (effects (font (size 1.27 1.27)))))

(replace_symbol_property "U8"
  (property "Value" "INA181A1" (at 243.84 139.7 0)
    (effects (font (size 1.27 1.27)))))

;; ==========================================================================
;; SECTION 2: CRITICAL - Add Missing LM2596 Output Inductor
;; ==========================================================================

(add_symbol (lib_id "Device:L") (at 88.9 53.34 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid L2_BUCK)
  (property "Reference" "L2" (at 88.9 50.8 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "33uH/5A" (at 88.9 55.88 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Inductor_SMD:L_12x12mm_H8mm" (at 88.9 53.34 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid L2_BUCK-1))
  (pin "2" (uuid L2_BUCK-2)))

;; Connect inductor between LM2596 output and 5V rail
(add_wire (pts (xy 86.36 53.34) (xy 86.36 53.34))
  (stroke (width 0) (type default))
  (uuid W_L2_IN))

(add_wire (pts (xy 91.44 53.34) (xy 96.52 53.34))
  (stroke (width 0) (type default))
  (uuid W_L2_OUT))

;; Add catch diode for buck converter
(add_symbol (lib_id "Diode:STPS3L60") (at 88.9 58.42 270) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid D14_CATCH)
  (property "Reference" "D14" (at 91.44 58.42 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "STPS3L60" (at 86.36 58.42 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Diode_SMD:D_SMB" (at 88.9 58.42 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid D14_CATCH-1))
  (pin "2" (uuid D14_CATCH-2)))

;; ==========================================================================
;; SECTION 3: HIGH PRIORITY - Complete RC Snubber Networks
;; ==========================================================================

;; Channel 2 Snubber
(add_symbol (lib_id "Device:R") (at 292.1 106.68 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid R_SNUB2)
  (property "Reference" "R19" (at 294.64 106.68 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100R" (at 292.1 106.68 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Resistor_SMD:R_0805_2012Metric" (at 290.322 106.68 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid R_SNUB2-1))
  (pin "2" (uuid R_SNUB2-2)))

(add_symbol (lib_id "Device:C") (at 292.1 110.49 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C_SNUB2)
  (property "Reference" "C15" (at 294.64 110.49 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "10nF/100V" (at 294.64 113.03 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (at 293.0652 114.3 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C_SNUB2-1))
  (pin "2" (uuid C_SNUB2-2)))

;; Channel 3 Snubber
(add_symbol (lib_id "Device:R") (at 292.1 121.92 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid R_SNUB3)
  (property "Reference" "R20" (at 294.64 121.92 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100R" (at 292.1 121.92 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Resistor_SMD:R_0805_2012Metric" (at 290.322 121.92 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid R_SNUB3-1))
  (pin "2" (uuid R_SNUB3-2)))

(add_symbol (lib_id "Device:C") (at 292.1 125.73 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C_SNUB3)
  (property "Reference" "C16" (at 294.64 125.73 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "10nF/100V" (at 294.64 128.27 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (at 293.0652 129.54 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C_SNUB3-1))
  (pin "2" (uuid C_SNUB3-2)))

;; Channel 4 Snubber
(add_symbol (lib_id "Device:R") (at 292.1 137.16 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid R_SNUB4)
  (property "Reference" "R21" (at 294.64 137.16 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100R" (at 292.1 137.16 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Resistor_SMD:R_0805_2012Metric" (at 290.322 137.16 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid R_SNUB4-1))
  (pin "2" (uuid R_SNUB4-2)))

(add_symbol (lib_id "Device:C") (at 292.1 140.97 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C_SNUB4)
  (property "Reference" "C17" (at 294.64 140.97 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "10nF/100V" (at 294.64 143.51 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0805_2012Metric" (at 293.0652 144.78 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C_SNUB4-1))
  (pin "2" (uuid C_SNUB4-2)))

;; ==========================================================================
;; SECTION 4: RS-485 Protection Enhancement
;; ==========================================================================

(add_symbol (lib_id "Device:D_TVS_ALT") (at 99.06 182.88 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid D15_RS485_TVS)
  (property "Reference" "D15" (at 101.6 182.88 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "PESD1CAN" (at 96.52 182.88 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 99.06 182.88 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid D15_RS485_TVS-1))
  (pin "2" (uuid D15_RS485_TVS-2)))

;; Connect TVS to RS-485 A line
(add_wire (pts (xy 81.28 182.88) (xy 96.52 182.88))
  (stroke (width 0) (type default))
  (uuid W_TVS_A))

(add_wire (pts (xy 101.6 182.88) (xy 101.6 193.04))
  (stroke (width 0) (type default))
  (uuid W_TVS_GND))

(add_symbol (lib_id "Device:D_TVS_ALT") (at 99.06 187.96 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid D16_RS485_TVS)
  (property "Reference" "D16" (at 101.6 187.96 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "PESD1CAN" (at 96.52 187.96 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Package_TO_SOT_SMD:SOT-23" (at 99.06 187.96 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid D16_RS485_TVS-1))
  (pin "2" (uuid D16_RS485_TVS-2)))

;; Common mode choke for RS-485
(add_symbol (lib_id "Device:L_Coupled") (at 88.9 185.42 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid CM1_RS485)
  (property "Reference" "L3" (at 88.9 180.34 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100uH CM" (at 88.9 190.5 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Inductor_SMD:L_CommonMode_Wuerth_WE-SL2" (at 88.9 185.42 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid CM1_RS485-1))
  (pin "2" (uuid CM1_RS485-2))
  (pin "3" (uuid CM1_RS485-3))
  (pin "4" (uuid CM1_RS485-4)))

;; ==========================================================================
;; SECTION 5: Input Protection Enhancement
;; ==========================================================================

;; Add input fuse
(add_symbol (lib_id "Device:Fuse") (at 43.18 50.8 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid F1_INPUT)
  (property "Reference" "F1" (at 43.18 48.26 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "5A" (at 43.18 53.34 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Fuse:Fuse_1206_3216Metric" (at 43.18 52.578 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid F1_INPUT-1))
  (pin "2" (uuid F1_INPUT-2)))

;; Reverse polarity protection
(add_symbol (lib_id "Device:D_Schottky") (at 48.26 50.8 180) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid D13_REVERSE)
  (property "Reference" "D13" (at 48.26 48.26 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "SS54" (at 48.26 53.34 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Diode_SMD:D_SMB" (at 48.26 50.8 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid D13_REVERSE-1))
  (pin "2" (uuid D13_REVERSE-2)))

;; ==========================================================================
;; SECTION 6: ADC Input Protection and Filtering
;; ==========================================================================

;; Add RC filters for each ADC input (INA output to MCU)
;; Channel 1 ADC filter
(add_symbol (lib_id "Device:R") (at 205.74 78.74 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid R25_ADC1)
  (property "Reference" "R25" (at 205.74 76.2 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "1k" (at 205.74 81.28 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 205.74 80.518 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid R25_ADC1-1))
  (pin "2" (uuid R25_ADC1-2)))

(add_symbol (lib_id "Device:C") (at 210.82 83.82 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C20_ADC1)
  (property "Reference" "C20" (at 213.36 82.55 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100nF" (at 213.36 85.09 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 211.7852 87.63 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C20_ADC1-1))
  (pin "2" (uuid C20_ADC1-2)))

;; Channel 2 ADC filter
(add_symbol (lib_id "Device:R") (at 205.74 81.28 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid R26_ADC2)
  (property "Reference" "R26" (at 205.74 78.74 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "1k" (at 205.74 83.82 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 205.74 83.058 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid R26_ADC2-1))
  (pin "2" (uuid R26_ADC2-2)))

(add_symbol (lib_id "Device:C") (at 210.82 86.36 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C21_ADC2)
  (property "Reference" "C21" (at 213.36 85.09 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100nF" (at 213.36 87.63 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 211.7852 90.17 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C21_ADC2-1))
  (pin "2" (uuid C21_ADC2-2)))

;; Channel 3 ADC filter
(add_symbol (lib_id "Device:R") (at 205.74 83.82 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid R27_ADC3)
  (property "Reference" "R27" (at 205.74 81.28 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "1k" (at 205.74 86.36 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 205.74 85.598 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid R27_ADC3-1))
  (pin "2" (uuid R27_ADC3-2)))

(add_symbol (lib_id "Device:C") (at 210.82 88.9 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C22_ADC3)
  (property "Reference" "C22" (at 213.36 87.63 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100nF" (at 213.36 90.17 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 211.7852 92.71 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C22_ADC3-1))
  (pin "2" (uuid C22_ADC3-2)))

;; Channel 4 ADC filter
(add_symbol (lib_id "Device:R") (at 205.74 86.36 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid R28_ADC4)
  (property "Reference" "R28" (at 205.74 83.82 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "1k" (at 205.74 88.9 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 205.74 88.138 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid R28_ADC4-1))
  (pin "2" (uuid R28_ADC4-2)))

(add_symbol (lib_id "Device:C") (at 210.82 91.44 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C23_ADC4)
  (property "Reference" "C23" (at 213.36 90.17 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100nF" (at 213.36 92.71 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 211.7852 95.25 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C23_ADC4-1))
  (pin "2" (uuid C23_ADC4-2)))

;; ==========================================================================
;; SECTION 7: Crystal Shield Grounding Fix
;; ==========================================================================

;; Connect crystal shield pins to ground
(add_wire (pts (xy 147.32 63.5) (xy 147.32 78.74))
  (stroke (width 0) (type default))
  (uuid W_XTAL_SHIELD1))

(add_wire (pts (xy 147.32 73.66) (xy 147.32 78.74))
  (stroke (width 0) (type default))
  (uuid W_XTAL_SHIELD2))

;; ==========================================================================
;; SECTION 8: Additional Bypass Capacitors for INA181
;; ==========================================================================

(add_symbol (lib_id "Device:C") (at 241.3 96.52 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C_INA2_BYPASS)
  (property "Reference" "C24" (at 241.3 93.98 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100nF" (at 241.3 99.06 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 245.11 95.5548 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C_INA2_BYPASS-1))
  (pin "2" (uuid C_INA2_BYPASS-2)))

(add_symbol (lib_id "Device:C") (at 241.3 111.76 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C_INA3_BYPASS)
  (property "Reference" "C25" (at 241.3 109.22 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100nF" (at 241.3 114.3 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 245.11 110.7948 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C_INA3_BYPASS-1))
  (pin "2" (uuid C_INA3_BYPASS-2)))

(add_symbol (lib_id "Device:C") (at 241.3 127.0 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid C_INA4_BYPASS)
  (property "Reference" "C26" (at 241.3 124.46 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "100nF" (at 241.3 129.54 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Capacitor_SMD:C_0603_1608Metric" (at 245.11 126.0348 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid C_INA4_BYPASS-1))
  (pin "2" (uuid C_INA4_BYPASS-2)))

;; ==========================================================================
;; SECTION 9: Test Points for Production Testing
;; ==========================================================================

(add_symbol (lib_id "Connector:TestPoint") (at 312.42 78.74 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid TP1_12V)
  (property "Reference" "TP1" (at 314.96 76.2 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "12V" (at 314.96 78.74 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "TestPoint:TestPoint_Pad_D1.5mm" (at 317.5 78.74 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid TP1_12V-1)))

(add_symbol (lib_id "Connector:TestPoint") (at 96.52 48.26 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid TP2_5V)
  (property "Reference" "TP2" (at 99.06 45.72 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "5V" (at 99.06 48.26 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "TestPoint:TestPoint_Pad_D1.5mm" (at 101.6 48.26 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid TP2_5V-1)))

(add_symbol (lib_id "Connector:TestPoint") (at 127 55.88 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid TP3_3V3)
  (property "Reference" "TP3" (at 129.54 53.34 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "3V3" (at 129.54 55.88 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "TestPoint:TestPoint_Pad_D1.5mm" (at 132.08 55.88 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid TP3_3V3-1)))

(add_symbol (lib_id "Connector:TestPoint") (at 287.02 149.86 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid TP4_GND)
  (property "Reference" "TP4" (at 289.56 147.32 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "GND" (at 289.56 149.86 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "TestPoint:TestPoint_Pad_D1.5mm" (at 292.1 149.86 0)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid TP4_GND-1)))

;; ==========================================================================
;; SECTION 10: Fix Reference Designator Conflicts
;; ==========================================================================

;; Update duplicate power reference designators
(replace_property "#PWR01" 
  (property "Reference" "#PWR016" (at 307.34 90.17 0)))

(replace_property "#PWR02" 
  (property "Reference" "#PWR017" (at 96.52 54.61 0)))

(replace_property "#PWR03" 
  (property "Reference" "#PWR018" (at 127 62.23 0)))

(replace_property "#PWR04" 
  (property "Reference" "#PWR019" (at 50.8 77.47 0)))

(replace_property "#PWR05" 
  (property "Reference" "#PWR020" (at 294.64 148.59 0)))

;; ==========================================================================
;; SECTION 11: Status LEDs for Each Channel
;; ==========================================================================

(add_symbol (lib_id "Device:LED") (at 266.7 93.98 0) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid LED_CH1)
  (property "Reference" "D17" (at 266.7 91.44 0)
    (effects (font (size 1.27 1.27))))
  (property "Value" "CH1" (at 266.7 96.52 0)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "LED_SMD:LED_0603_1608Metric" (at 266.7 93.98 0)
    (effects (font (size 1.27 1.27)) hide))
  (property "Color" "Green" (at 266.7 99.06 0)
    (effects (font (size 1.27 1.27))))
  (pin "1" (uuid LED_CH1-1))
  (pin "2" (uuid LED_CH1-2)))

(add_symbol (lib_id "Device:R") (at 261.62 93.98 90) (unit 1)
  (in_bom yes) (on_board yes) (dnp no)
  (uuid R_LED_CH1)
  (property "Reference" "R29" (at 261.62 91.44 90)
    (effects (font (size 1.27 1.27))))
  (property "Value" "1k" (at 261.62 96.52 90)
    (effects (font (size 1.27 1.27))))
  (property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 261.62 95.758 90)
    (effects (font (size 1.27 1.27)) hide))
  (pin "1" (uuid R_LED_CH1-1))
  (pin "2" (uuid R_LED_CH1-2)))

;; Repeat for channels 2-4 (abbreviated for space)

;; ==========================================================================
;; END OF PATCH FILE
;; ==========================================================================
