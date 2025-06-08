from opentrons import protocol_api

#define metadata
metadata = {
    "apiLevel": "2.20",
    "protocolName": "serial dilution",
    "description": """protocol to perfrom serial dilution using 8-channel pipette with 
    washing steps and tip return steps to reduce waste""",
    "author": "Group 1"
    }

def run(protocol: protocol_api.ProtocolContext):
    # define labware, only multi pipette was used
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", 3)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 2)
    reservoir_wash = protocol.load_labware("nest_12_reservoir_15ml",6)
    platform = protocol.load_labware("nest_12_reservoir_15ml", 1)
    right_pipette = protocol.load_instrument("p300_multi_gen2", "right", tip_racks=[tips])

    # fill water to all well
    right_pipette.pick_up_tip()
    right_pipette.transfer(250, reservoir.rows()[0][8:11],
                                platform.rows()[0],
                                new_tip="never")
    right_pipette.return_tip()
    
# fill solvent with mixing
    right_pipette.pick_up_tip()
    right_pipette.transfer(250,  [reservoir["A1"]], 
                                  [platform["A1"],
                                 platform["A2"],
                                 platform["A3"]],
                                mix_after=(3, 200),
                                push_out=True,
                                new_tip="never")
    # clean the tip before returning to tip rack
    right_pipette.transfer(300,  reservoir_wash["A1"],  reservoir_wash["A2"], new_tip="never")
    right_pipette.return_tip()
    # dilution
    right_pipette.pick_up_tip()
    right_pipette.transfer(250,  [platform["A1"],
                                 platform["A2"],
                                 platform["A3"]],
                                  [platform["A4"],
                                 platform["A5"],
                                 platform["A6"]],
                                 new_tip="never",
                                 mix_after=(3, 200),
                                 push_out=True)
    # clean the tip before returning to tip rack
    right_pipette.transfer(300,  reservoir_wash["A3"],   reservoir_wash["A4"], new_tip="never")
    right_pipette.return_tip()

    # dilution
    right_pipette.pick_up_tip()
    right_pipette.transfer(250,  [platform["A4"],
                                 platform["A5"],
                                 platform["A6"]],
                                  [platform["A7"],
                                 platform["A8"],
                                 platform["A9"]],
                                 new_tip="never",
                                 mix_after=(3, 200),
                                 push_out=True)
    # clean the tip before returning to tip rack
    right_pipette.transfer(300,  reservoir_wash["A5"],   reservoir_wash["A6"], new_tip="never")
    right_pipette.return_tip()

    # dilution
    right_pipette.pick_up_tip()
    right_pipette.transfer(250,  [platform["A7"],
                                 platform["A8"],
                                 platform["A9"]],
                                  [platform["A10"],
                                 platform["A11"],
                                 platform["A12"]],
                                 new_tip="never",
                                 mix_after=(3, 200),
                                 push_out=True)
    
    # clean the tip before returning to tip rack
    right_pipette.transfer(300,  reservoir_wash["A7"],   reservoir_wash["A8"], new_tip="never")
    right_pipette.return_tip()

