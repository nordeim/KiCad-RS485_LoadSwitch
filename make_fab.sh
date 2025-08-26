#!/usr/bin/env bash
set -euo pipefail

PROJ="RS485_LoadSwitch"
PCB="${PROJ}.kicad_pcb"
SCH="RS485_LoadSwitch_Main.kicad_sch"
REL="Release_${PROJ}_RevA_$(date +%Y%m%d)"

mkdir -p "fab/${REL}/gerbers" "fab/${REL}/drill" "fab/${REL}/assembly" "fab/${REL}/3d" "fab/${REL}/docs"

# Set board origin to lower-left of outline in KiCad before running for consistent XY.

# Gerbers
kicad-cli pcb export gerbers "${PCB}" \
  --output "fab/${REL}/gerbers" \
  --layers F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts,F.Paste,B.Paste \
  --subtract-soldermask \
  --no-x2

# Drills
kicad-cli pcb export drill "${PCB}" \
  --output "fab/${REL}/drill" \
  --format excellon \
  --drill-origin absolute \
  --generate-map \
  --map-format pdf \
  --unit mm \
  --mirror

# 3D STEP
kicad-cli pcb export step "${PCB}" \
  --subst-models \
  --output "fab/${REL}/3d/${PROJ}_RevA.step"

# Assembly PDFs (overlay of F.Fab + F.SilkS + Edge.Cuts)
kicad-cli pcb export pdf "${PCB}" \
  --output "fab/${REL}/assembly/${PROJ}_Assembly_Top.pdf" \
  --layers F.Fab,F.SilkS,Edge.Cuts
kicad-cli pcb export pdf "${PCB}" \
  --output "fab/${REL}/assembly/${PROJ}_Assembly_Bot.pdf" \
  --layers B.Fab,B.SilkS,Edge.Cuts

# Pick-and-place (centroid)
kicad-cli pcb export pos "${PCB}" \
  --output "fab/${REL}/assembly/${PROJ}_Top.pos" \
  --format csv --units mm --side front
kicad-cli pcb export pos "${PCB}" \
  --output "fab/${REL}/assembly/${PROJ}_Bot.pos" \
  --format csv --units mm --side back

# BOM (grouped)
# Requires KiCad bom plugins; fallback is schematic CSV
kicad-cli sch export bom "${SCH}" \
  --output "fab/${REL}/assembly/${PROJ}_BOM.csv" \
  --format csv

# Fabrication drawing (dimensions should be on Dwgs.User)
kicad-cli pcb export pdf "${PCB}" \
  --output "fab/${REL}/docs/${PROJ}_Fabrication_Drawing.pdf" \
  --layers Dwgs.User,Edge.Cuts,F.Cu,B.Cu,User.Comments

# Zip for fab
( cd "fab/${REL}" && zip -r "../${REL}.zip" . )
echo "Fabrication package at fab/${REL}.zip"
