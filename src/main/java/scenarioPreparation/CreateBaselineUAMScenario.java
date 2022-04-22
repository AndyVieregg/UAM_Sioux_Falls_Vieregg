package scenarioPreparation;

import net.bhl.matsim.uam.scenario.RunCreateUAMBeelineScenario;

public class CreateBaselineUAMScenario {

	public static void main(String[] args) {
		
		String linkFreespeed = "42";
		String linkCapacity = "9999";
		
		
		String[] createScenarioArgs = new String [6];
		int j = 0;
		String inputPath = "original-input-data/sioux_falls";
		
		createScenarioArgs[j++] = inputPath + "/config.xml";
		createScenarioArgs[j++] = inputPath + "/stations.csv";
		createScenarioArgs[j++] = linkFreespeed;
		createScenarioArgs[j++] = linkCapacity;
		createScenarioArgs[j++] = inputPath + "/vehicles.csv";
		
		
		RunCreateUAMBeelineScenario.main(createScenarioArgs);
		
		
	}
}
