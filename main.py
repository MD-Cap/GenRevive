import logging
import sys


## add here all imports

## step 1 - create asp.net mvc project template
from activities.dotnet_project_template_creator.dotnet_project_template_creator import DotNetProjectTemplateCreator
## step 2 - generate migrated code where source is vb6 and target is ASP.NET MVC
from activities.vb_to_dotnet_code_generator.vbtodotnetcode_generator import VBToDotNetCodeGenerator
## step 3 - shift AI generated code from staging location into the target ASP.NET MVC project; also make necessary changes 
from activities.shift_code_in_target_location_and_make_changes.shiftcodeintargetlocation_and_makechanges import ShiftCodeInTargetLocationAndMakeChanges
## step 4 - Add db context and Dependency Injectiion (DI) code in the MVC project (target location)
from activities.add_dbContext_di_code_in_target_locations.add_dbContext_di_code_in_target_locations import AddDBContextDICodeInTargetLocations
## step 5 - Add unit tests using AI assistent
from activities.dotnet_code_generator_unit_test.dotnet_code_generator_unit_test import DotnetCodeGeneratorUnitTests


from dotenv.main import load_dotenv
from genrevive.helpers.common.logger import Logger

logging.root.setLevel(level=logging.INFO)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    load_dotenv()
    sys.stdout = Logger()

    DotNetProjectTemplateCreator().execute() #create .net mvc project template ....
    VBToDotNetCodeGenerator().execute() # Generate code using AI assistent where source is vb6 and target is ASP.NET MVC; target location is staging location
    ShiftCodeInTargetLocationAndMakeChanges().execute() # move AI generated code inside mvc project folder structure
    AddDBContextDICodeInTargetLocations().execute() # add db context class for EF and add DI in the program.cs
    DotnetCodeGeneratorUnitTests().execute() # generate code in unit test project
    
    
    
    


