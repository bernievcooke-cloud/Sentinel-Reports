import sys
import surf_worker
import sky_worker

# sys.argv[0] is the script name
# sys.argv[1] is the Report Type
# sys.argv[2] is the Location
# sys.argv[3] is the Phone Number

report_type = sys.argv[1]
location = sys.argv[2]
phone = sys.argv[3]

if report_type == "Surf Strategy":
    # Run your Surf PDF logic
    surf_worker.run_full_automation(location, phone)
elif report_type == "Night Sky":
    # Run your Sky PDF logic
    sky_worker.run_full_automation(location, phone)