package analysis;

import org.matsim.contrib.otfvis.OTFVis;

public class VisualiseMobsim {

	public static void main(String[] args) {
		java.util.logging.Logger logger = java.util.logging.Logger.getLogger("VisualiseIteration");
		
		int iterationNo = 500;
		String scenarioPath = "scenarios/sioux_falls_uam";
		
		String[] convertArgs = new String [5];
		
		convertArgs[1] = scenarioPath + String.format("/output/ITERS/it.%d/%d.events.xml.gz",iterationNo, iterationNo);	// event file to replay
		convertArgs[2] = scenarioPath + "/uam_network.xml.gz";							// network file on which to replay
		convertArgs[3] = scenarioPath + String.format("/output/ITERS/it.%d/%d.visualisation.mvi",iterationNo, iterationNo);
		convertArgs[4] = "60";
		
		OTFVis.convert(convertArgs);
		
		logger.info("MVI file created. Starting visualisation.");
		
		OTFVis.playMVI(scenarioPath + String.format("/output/ITERS/it.%d/%d.visualisation.mvi",iterationNo, iterationNo));

	}

}
