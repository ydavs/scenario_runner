import argparse
from argparse import RawTextHelpFormatter
import sys
import subprocess
from typing import List


REMOVED_ARGUMETS: List[str] = ["positionSeed", "positionSeedRangeMin", "positionSeedRangeMax"]


if __name__ == "__main__":

    # pylint: disable=line-too-long
    # @comment: Let the parser alone!
    parser = argparse.ArgumentParser(description=(),
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version='')
    parser.add_argument('--host', default='127.0.0.1',
                        help='IP of the host server (default: localhost)')
    parser.add_argument('--port', default='2000',
                        help='TCP port to listen to (default: 2000)')
    parser.add_argument('--timeout', default="10.0",
                        help='Set the CARLA client timeout value in seconds')
    parser.add_argument('--trafficManagerPort', default='8000',
                        help='Port to use for the TrafficManager (default: 8000)')
    parser.add_argument('--trafficManagerSeed', default='0',
                        help='Seed used by the TrafficManager (default: 0)')
    parser.add_argument('--sync', action='store_true',
                        help='Forces the simulation to run synchronously')
    parser.add_argument('--list', action="store_true", help='List all supported scenarios and exit')

    parser.add_argument(
        '--scenario', help='Name of the scenario to be executed. Use the preposition \'group:\' to run all scenarios of one class, e.g. ControlLoss or FollowLeadingVehicle')
    parser.add_argument('--openscenario2', help='Provide an openscenario2 definition')
    parser.add_argument('--route', help='Run a route as a scenario', type=str)
    parser.add_argument('--route-id', help='Run a specific route inside that \'route\' file', default='', type=str)
    parser.add_argument(
        '--agent', help="Agent used to execute the route. Not compatible with non-route-based scenarios.")
    parser.add_argument('--agentConfig', type=str, help="Path to Agent's configuration file", default="")

    parser.add_argument('--output', action="store_true", help='Provide results on stdout')
    parser.add_argument('--file', action="store_true", help='Write results into a txt file')
    parser.add_argument('--junit', action="store_true", help='Write results into a junit file')
    parser.add_argument('--json', action="store_true", help='Write results into a JSON file')
    parser.add_argument('--outputDir', default='', help='Directory for output files (default: this directory)')

    parser.add_argument('--configFile', default='', help='Provide an additional scenario configuration file (*.xml)')
    parser.add_argument('--additionalScenario', default='', help='Provide additional scenario implementations (*.py)')

    parser.add_argument('--debug', action="store_true", help='Run with debug output')
    parser.add_argument('--reloadWorld', action="store_true",
                        help='Reload the CARLA world before starting a scenario (default=True)')
    parser.add_argument('--record', type=str, default='',
                        help='Path were the files will be saved, relative to SCENARIO_RUNNER_ROOT.\nActivates the CARLA recording feature and saves to file all the criteria information.')
    parser.add_argument('--randomize', action="store_true", help='Scenario parameters are randomized')
    parser.add_argument('--repetitions', default=1, type=int, help='Number of scenario executions')
    parser.add_argument('--waitForEgo', action="store_true", help='Connect the scenario to an existing ego vehicle')
    parser.add_argument('--positionSeed', default=0, type=int, help='Position seed selected for the scenario execution')
    parser.add_argument('--positionSeedRangeMin', default=0, type=int, help='If Range what is the minimum of the position seed')
    parser.add_argument('--positionSeedRangeMax', default=0, type=int, help='If range what is the maximum of the position seed')

    arguments = parser.parse_args()

    minimum: int
    maximum: int
    if arguments.positionSeedRangeMin == arguments.positionSeedRangeMax:
        minimum, maximum = arguments.positionSeed, arguments.positionSeed + 1
    elif arguments.positionSeedRangeMin > arguments.positionSeedRangeMax:
        # Incorrect Arguments
        print(f"Incorrect arguments provided, position seed min is greater than position seed max. {arguments.positionSeedRangeMin} > {arguments.positionSeedRangeMax}")
        sys.exit()
    else:
        minimum, maximum = arguments.positionSeedRangeMin, arguments.positionSeedRangeMax

    

    for i in range(minimum, maximum, 1):
        print(f"-------------------------- POSITION SEED : {i} --------------------------")
        command: str = "python scenario_runner.py "
        for arg_name, arg_value in arguments._get_kwargs():
            if (arg_value is None or
                arg_value == "" or
                arg_name in REMOVED_ARGUMETS or
                arg_value is False):
                continue
            
            # if isinstance(arg_value, str):
            #     command += f"-- {arg_name} '{arg_value}' "
            # else:
            if arg_value is True:
                command += f"--{arg_name} "
            else:
                command += f"--{arg_name} {arg_value} "
        command += f"--positionSeed {i}"
        subprocess.run(command, check=True)