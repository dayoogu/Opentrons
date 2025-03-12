import subprocess

# Define file paths
protocol_path = r"C:\Eileen\Opentron\UCL.py"
output_path = r"C:\Eileen\simulation_result_UCL.txt"

try:
    # Run the Opentrons simulation command
    result = subprocess.run(
        ["opentrons_simulate", protocol_path],
        capture_output=True, text=True, encoding="latin-1"  # Change encoding to avoid Unicode errors
    )

    # Save the output to a text file
    with open(output_path, "w", encoding="utf-8", errors="replace") as output_file:
        output_file.write(result.stdout)

    print(f"✅ Simulation steps saved successfully to: {output_path}")

except Exception as e:
    print(f"❌ Error occurred: {e}")
