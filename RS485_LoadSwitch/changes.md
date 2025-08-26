awesome job! please put on your deep thinking hat to deeply think and thoroughly and carefully review the "diff" output of the files below and double-check and validate the changes, make sure the changes are correct and accurate. 

$ diff -u backup/Power.kicad_sch Power.kicad_sch
--- backup/Power.kicad_sch      2025-08-26 22:07:42.853431978 +0800
+++ Power.kicad_sch     2025-08-26 22:18:29.025218799 +0800
@@ -23,8 +23,8 @@
     (property "Reference" "U1")(property "Value" "LM2596S-5.0")
   )
   (symbol (lib_id "Device:L") (at 160 50) (property "Reference" "L1")(property "Value" "33uH"))
-  (symbol (lib_id "Diode:D_Schottky") (at 160 60) (property "Reference" "D_BK")(property "Value" "MBR360"))
   (symbol (lib_id "Device:C") (at 120 70) (property "Reference" "CIN")(property "Value" "100uF/35V"))
+  (symbol (lib_id "Device:D_Schottky") (at 160 60) (property "Reference" "D_BK")(property "Value" "MBR360"))
   (symbol (lib_id "Device:C") (at 175 70) (property "Reference" "COUT1")(property "Value" "330uF/10V"))
   (symbol (lib_id "Device:C") (at 175 75) (property "Reference" "COUT2")(property "Value" "22uF"))
 
@@ -37,5 +37,4 @@
   (symbol (lib_id "Device:C") (at 195 70) (property "Reference" "C_LDO_IN")(property "Value" "1uF"))
   (symbol (lib_id "Device:C") (at 205 70) (property "Reference" "C_LDO_OUT")(property "Value" "1uF"))
   (global_label (at 210 50) (text "+3V3"))
-
 )

$ diff -u backup/RS485_LoadSwitch.kicad_pcb RS485_LoadSwitch.kicad_pcb
--- backup/RS485_LoadSwitch.kicad_pcb   2025-08-26 22:07:42.853431978 +0800
+++ RS485_LoadSwitch.kicad_pcb  2025-08-26 22:26:37.357845501 +0800
@@ -81,7 +81,6 @@
     (connect_pads (clearance 0.4)) (min_thickness 0.3)
     (polygon (pts (xy 60 0) (xy 100 0) (xy 100 80) (xy 60 80))))
 
-
   (footprint "Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical" (layer "F.Cu") (at 5 10)
     (attr through_hole)
     (fp_text reference "J1" (at 0 -3))
@@ -94,9 +93,9 @@
   (footprint "Package_TO_SOT_THT:TO-220-3_Vertical" (layer "F.Cu") (at 20 15)
     (attr through_hole)
     (fp_text reference "QRP")(fp_text value "IRF4905")
-    (pad "1" thru_hole rect (at 0 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 3 "+12V_RAIL"))  ; G
-    (pad "2" thru_hole oval (at 2.54 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 2 "+12V_IN"))   ; D
-    (pad "3" thru_hole oval (at 5.08 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 3 "+12V_RAIL"))  ; S
+    (pad "1" thru_hole rect (at 0 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 3 "+12V_RAIL"))
+    (pad "2" thru_hole oval (at 2.54 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 2 "+12V_IN"))
+    (pad "3" thru_hole oval (at 5.08 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 3 "+12V_RAIL"))
   )
 
   (footprint "Diode_SMD:D_SMB" (layer "F.Cu") (at 15 25)
@@ -179,9 +178,9 @@
 
   (footprint "Package_TO_SOT_THT:TO-220-3_Vertical" (layer "F.Cu") (at 85 20)
     (fp_text reference "Q1")(fp_text value "IRLZ44N")
-    (pad "1" thru_hole rect (at 0 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask)) ; G via TC4468 OUT1
-    (pad "2" thru_hole oval (at 2.54 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 15 "OUT1")) ; D
-    (pad "3" thru_hole oval (at 5.08 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 1 "GND")) ; S via shunt
+    (pad "1" thru_hole rect (at 0 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask))
+    (pad "2" thru_hole oval (at 2.54 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 15 "OUT1"))
+    (pad "3" thru_hole oval (at 5.08 0) (size 1.7 2.0) (drill 1.0) (layers *.Cu *.Mask) (net 1 "GND"))
   )
   (footprint "Resistor_SMD:R_2512_6332Metric" (layer "F.Cu") (at 90 28)
     (fp_text reference "R_SHUNT1")(fp_text value "0.05R")
@@ -204,13 +203,12 @@
     (pad "2" thru_hole circle (at 3.96 0) (size 2.6 2.6) (drill 1.3) (layers *.Cu *.Mask) (net 15 "OUT1"))
   )
 
-
   (via (at 50 50) (size 1.2) (drill 0.6) (layers "F.Cu" "B.Cu") (net 1))
   (via (at 60 50) (size 1.2) (drill 0.6) (layers "F.Cu" "B.Cu") (net 1))
 
-  (segment (start 5 10) (end 20 15) (width 1.0) (layer "F.Cu") (net 2)) ; +12V_IN to PFET
-  (segment (start 25 15) (end 60 15) (width 2.5) (layer "F.Cu") (net 3)) ; +12V_RAIL spine
-  (segment (start 95 10) (end 95 15) (width 3.0) (layer "F.Cu") (net 3)) ; to outputs
+  (segment (start 5 10) (end 20 15) (width 1.0) (layer "F.Cu") (net 2))
+  (segment (start 25 15) (end 60 15) (width 2.5) (layer "F.Cu") (net 3))
+  (segment (start 95 10) (end 95 15) (width 3.0) (layer "F.Cu") (net 3))
 
   (gr_text "RS-485 4-CH 12V Load Ctrl / PWM" (at 50 78) (layer "F.SilkS") (size 1.5 1.5) (thickness 0.25))
 )

$ diff -u backup/sym-lib-table sym-lib-table
--- backup/sym-lib-table        2025-08-26 22:02:19.466134054 +0800
+++ sym-lib-table       2025-08-26 22:30:25.247839247 +0800
@@ -1,10 +1,10 @@
 (sym_lib_table
-  (lib (name "Device")(type "Legacy")(uri "${KICAD8_SYMBOL_DIR}/Device.kicad_sym")(options "")(descr ""))
-  (lib (name "Connector")(type "Legacy")(uri "${KICAD8_SYMBOL_DIR}/Connector.kicad_sym")(options "")(descr ""))
-  (lib (name "MCU_ST_STM32")(type "Legacy")(uri "${KICAD8_SYMBOL_DIR}/MCU_ST_STM32.kicad_sym")(options "")(descr ""))
-  (lib (name "Interface_UART")(type "Legacy")(uri "${KICAD8_SYMBOL_DIR}/Interface_UART.kicad_sym")(options "")(descr ""))
-  (lib (name "Regulator_Linear")(type "Legacy")(uri "${KICAD8_SYMBOL_DIR}/Regulator_Linear.kicad_sym")(options "")(descr ""))
-  (lib (name "Regulator_Switching")(type "Legacy")(uri "${KICAD8_SYMBOL_DIR}/Regulator_Switching.kicad_sym")(options "")(descr ""))
-  (lib (name "Diode")(type "Legacy")(uri "${KICAD8_SYMBOL_DIR}/Diode.kicad_sym")(options "")(descr ""))
-  (lib (name "Power_Protection")(type "Legacy")(uri "${KICAD8_SYMBOL_DIR}/Power_Protection.kicad_sym")(options "")(descr ""))
+  (lib (name "Device")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Device.kicad_sym")(options "")(descr ""))
+  (lib (name "Connector")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Connector.kicad_sym")(options "")(descr ""))
+  (lib (name "MCU_ST_STM32")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/MCU_ST_STM32.kicad_sym")(options "")(descr ""))
+  (lib (name "Interface_UART")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Interface_UART.kicad_sym")(options "")(descr ""))
+  (lib (name "Regulator_Linear")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Regulator_Linear.kicad_sym")(options "")(descr ""))
+  (lib (name "Regulator_Switching")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Regulator_Switching.kicad_sym")(options "")(descr ""))
+  (lib (name "Diode")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Diode.kicad_sym")(options "")(descr ""))
+  (lib (name "Power_Protection")(type "KiCad")(uri "${KICAD8_SYMBOL_DIR}/Power_Protection.kicad_sym")(options "")(descr ""))
 )
