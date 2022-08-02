package scenarioPreparation;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.matsim.api.core.v01.Coord;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.network.Network;
import org.matsim.api.core.v01.population.Population;
import org.matsim.api.core.v01.population.PopulationWriter;
import org.matsim.api.core.v01.population.Activity;
import org.matsim.api.core.v01.population.Person;
import org.matsim.api.core.v01.population.Plan;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.population.PopulationUtils;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.core.utils.geometry.CoordUtils;

public class CreateTestPopulation {

	public static void main(String[] args) {
		
		String configPath = "scenarios/sf_pt_routing/config.xml";
		
		String outputNetworkPath = "scenarios/sf_pt_routing/poptest.xml";
		
		// load config and network
		Config config = ConfigUtils.loadConfig(configPath);
		Network network = ScenarioUtils.loadScenario(config).getNetwork();
	
		// initialise empty population
		Population population = PopulationUtils.createPopulation(config, network);
		
		// get centroid nodes' x and y location from csv
		Coord[] node_coords = new Coord[25];
		
		Reader in;
		Iterable<CSVRecord> records;
		try {
			in = new FileReader("src/main/resources/centroid_nodes.csv");
			records = CSVFormat.TDF.withHeader("zone_id","x","y","node_id").parse(in);
			
			int i = 1;
			for (CSVRecord record : records) {
				String node_x = record.get("x");
				String node_y = record.get("y");
				node_coords[i] = CoordUtils.createCoord(Double.parseDouble(node_x),Double.parseDouble(node_y));
				i++;		
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		// populate
		for(int o = 1; o <= 24; o++) {
			for(int d = 1; d <= 24; d++) {
				// get o and d coordinates
				
				// create plan
				Plan plan = PopulationUtils.createPlan();
				
				Activity home1 = PopulationUtils.createActivityFromCoord("home",node_coords[o]);
				home1.setEndTime(32400); // 09:00:00
				plan.addActivity(home1);
				
				PopulationUtils.createAndAddLeg(plan, "uam");
				
				Activity work1 = PopulationUtils.createActivityFromCoord("work",node_coords[d]);
				work1.setEndTime(61200); // 17:00:00
				plan.addActivity(work1);
				
				PopulationUtils.createAndAddLeg(plan, "uam");
				
				PopulationUtils.createAndAddActivityFromCoord(plan, "home", node_coords[o]);
				
				// add new person with the plan (and id o-d) to the population
				String idString = Integer.toString(o) + "-" + Integer.toString(d);
				Id<Person> id = Id.createPersonId(idString);
				Person person = PopulationUtils.getFactory().createPerson(id);
				person.addPlan(plan);
				PopulationUtils.putSubpopulation(person, "default");
				population.addPerson(person);
				
			}
		}
		
		// write output population
		new PopulationWriter(population,network).write(outputNetworkPath);
	}
	
}
