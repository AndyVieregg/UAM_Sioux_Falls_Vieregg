package analysis;

import org.matsim.contrib.otfvis.OTFVis;

public class VisualiseMobsim {

	public static void main(String[] args) {
		java.util.logging.Logger logger = java.util.logging.Logger.getLogger("VisualiseIteration");
		
		int iterationNo = 0;
		String scenarioPath = "scenarios/uam-test-scenario";
		
		String[] convertArgs = new String [5];
		
		convertArgs[1] = scenarioPath + String.format("/output/ITERS/it.%d/%d.events.xml.gz",iterationNo, iterationNo);	// event file to replay
		convertArgs[2] = scenarioPath + "/uam_routed_network.xml";							// network file on which to replay
		convertArgs[3] = scenarioPath + String.format("/output/ITERS/it.%d/%d.visualisation.mvi",iterationNo, iterationNo);
		convertArgs[4] = "60";
		
		OTFVis.convert(convertArgs);
		
		logger.info("MVI file created. Starting visualisation.");
		
		OTFVis.playMVI(scenarioPath + String.format("/output/ITERS/it.%d/%d.visualisation.mvi",iterationNo, iterationNo));

	}

}
