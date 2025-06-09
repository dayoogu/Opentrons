from opentrons import protocol_api
import time
# Experimental Condtion
# Temperature 75
# Ratio 1 3
# Initial Condition 0.3 0.5 

# Define Metadata
metadata = {
    "apiLevel": "2.16",
    "protocolName": "Automated AuNPs synthesis",
    "description": """protocol for automation of synthesis""",
    "author": "Group 1"
    }

def run(protocol: protocol_api.ProtocolContext):

    #define labware
    tip = protocol.load_labware("opentrons_96_tiprack_300ul", 2)
    tip2 = protocol.load_labware("opentrons_96_tiprack_300ul", 5)
    reservoir_water = protocol.load_labware("nest_12_reservoir_15ml", 4)
    reservoir_solution = protocol.load_labware("nest_12_reservoir_15ml", 3)
    plate = protocol.load_labware("nest_96_wellplate_2ml_deep", 1)
    circle_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 6)
    hs_mod = protocol.load_module(module_name="heaterShakerModuleV1", location="10")
    right_pipette = protocol.load_instrument("p300_multi_gen2", "right", tip_racks=[tip, tip2])
    
    #close heat shaker latch
    hs_mod.close_labware_latch()

    #Ask right pipette to pick up tip
    right_pipette.pick_up_tip()

    #Transfer water to target well
    #Transfer 980 ul of water to colume 2 of well plate
    right_pipette.transfer(300, reservoir_water["A1"], plate['A2'], new_tip='never')
    right_pipette.transfer(300, reservoir_water["A1"], plate['A2'], new_tip='never')
    right_pipette.transfer(300, reservoir_water["A2"], plate['A2'], new_tip='never')
    right_pipette.transfer(80, reservoir_water["A2"], plate['A2'], new_tip='never')
    
    #Transfer 980 ul of water to colume 3 of well plate
    right_pipette.transfer(300, reservoir_water["A3"], plate['A3'], new_tip='never')
    right_pipette.transfer(300, reservoir_water["A3"], plate['A3'], new_tip='never')
    right_pipette.transfer(300, reservoir_water["A4"], plate['A3'], new_tip='never')
    right_pipette.transfer(80, reservoir_water["A2"], plate['A3'], new_tip='never')
   
    #Transfer 980 ul of water to colume 4 of well plate
    right_pipette.transfer(300, reservoir_water["A4"], plate['A4'], new_tip='never')
    right_pipette.transfer(300, reservoir_water["A5"], plate['A4'], new_tip='never')
    right_pipette.transfer(100, reservoir_water["A2"], plate['A4'], new_tip='never')

    #Transfer 980 ul of water to colume 5 of well plate
    right_pipette.transfer(300, reservoir_water["A6"], plate['A5'], new_tip='never')
    right_pipette.transfer(300, reservoir_water["A6"], plate['A5'], new_tip='never')
    right_pipette.transfer(100, reservoir_water["A5"], plate['A5'], new_tip='never')

    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    
    #Transfer half of gold chloride from reservoir to well plate
    right_pipette.transfer(210, reservoir_solution["A1"], plate['A2'], new_tip='never')

    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    
    right_pipette.transfer(210, reservoir_solution["A1"], plate['A3'], new_tip='never')
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    
    right_pipette.transfer(300, reservoir_solution["A1"], plate['A4'], new_tip='never')
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    
    
    right_pipette.transfer(300, reservoir_solution["A2"], plate['A5'], new_tip='never')   
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    

    
    #Transfer sodium citrate to well plate
    
    right_pipette.transfer(37.06, reservoir_solution["A7"], plate['A2'], new_tip='never') 
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    
    right_pipette.transfer(12.35, reservoir_solution["A7"], plate['A3'], new_tip='never')
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    
    right_pipette.transfer(61.76, reservoir_solution["A7"], plate['A4'], new_tip='never')
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    
    right_pipette.transfer(20.59, reservoir_solution["A7"], plate['A5'], new_tip='never')
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
   
    #Transfer rest of the gold chloride from reservoir to well plate
    right_pipette.transfer(210, reservoir_solution["A3"], plate['A2'], new_tip='never', mix_after=(3, 50))
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    right_pipette.transfer(210, reservoir_solution["A3"], plate['A3'], new_tip='never', mix_after=(3, 50))
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    right_pipette.transfer(300, reservoir_solution["A3"], plate['A4'], new_tip='never')
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    right_pipette.transfer(100, reservoir_solution["A4"], plate['A4'], new_tip='never', mix_after=(3, 50))
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    right_pipette.transfer(300, reservoir_solution["A4"], plate['A5'], new_tip='never')
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    right_pipette.pick_up_tip()
    right_pipette.transfer(100, reservoir_solution["A4"], plate['A5'], new_tip='never', mix_after=(3, 50))
    #Ask right pipette to pick up tip
    right_pipette.drop_tip()  
    

    #open heat shaker latch
    hs_mod.open_labware_latch()

    #delay for 20 seconds to transfer labware onto the heat shaker
    protocol.delay(seconds=40)

    #close heat shaker latch
    hs_mod.close_labware_latch()

    #start heat shaker and stop protocol for 10 minues 
    hs_mod.set_and_wait_for_shake_speed(500)
    hs_mod.set_and_wait_for_temperature(90)
    protocol.delay(minutes=40)

    #stop heat shaker after 10 minutes
    hs_mod.deactivate_shaker()
    
    #open heat shaker latch
    hs_mod.open_labware_latch()

    #delay for 20 seconds to transfer labware back onto deck
    protocol.delay(seconds=40)

    #open heat shaker latch
    hs_mod.close_labware_latch()

    right_pipette.pick_up_tip()
    #transfer solution from plate to circle plate
    right_pipette.transfer(300, plate["A2"], circle_plate['A2'], new_tip='never')
    right_pipette.drop_tip()
    right_pipette.pick_up_tip()
    right_pipette.transfer(300, plate["A3"], circle_plate['A3'], new_tip='never')
    right_pipette.drop_tip()
    right_pipette.pick_up_tip()
    right_pipette.transfer(300, plate["A4"], circle_plate['A4'], new_tip='never')
    right_pipette.drop_tip()
    right_pipette.pick_up_tip()
    right_pipette.transfer(300, plate["A5"], circle_plate['A5'], new_tip='never')
    right_pipette.drop_tip()
    right_pipette.pick_up_tip()

    #add water to first column
    right_pipette.transfer(300, reservoir_water["A12"], circle_plate['A1'], new_tip='never')
    right_pipette.drop_tip()









    # transfer solution using single pipette to fill up remaining wells to complete UCL
    # left_pipette.pick_up_tip()
    # rowUp = plate.rows()[0]
    # rowDown = plate.rows()[7]

    # left_pipette.transfer(300, rowDown[0], rowDown[1], new_tip='never')
    # left_pipette.transfer(300, rowDown[3], rowDown[2], new_tip='never')

    # left_pipette.transfer(300, reservoir["A2"], rowUp[6], new_tip='never')
    # left_pipette.transfer(300, reservoir["A2"], rowUp[7], new_tip='never')

    # left_pipette.transfer(300, reservoir["A2"], rowDown[6], new_tip='never')
    # left_pipette.transfer(300, reservoir["A2"], rowDown[7], new_tip='never')

    # left_pipette.transfer(300, reservoir["A2"], rowDown[10], new_tip='never')
    # left_pipette.transfer(300, reservoir["A2"], rowDown[11], new_tip='never')
    # left_pipette.drop_tip()

