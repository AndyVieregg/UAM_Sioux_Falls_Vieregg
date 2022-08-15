package scenarioPreparation;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.matsim.api.core.v01.Coord;
import org.matsim.api.core.v01.Id;
import org.matsim.api.core.v01.Scenario;
import org.matsim.api.core.v01.network.Network;
import org.matsim.api.core.v01.population.Activity;
import org.matsim.api.core.v01.population.Person;
import org.matsim.api.core.v01.population.Plan;
import org.matsim.api.core.v01.population.Population;
import org.matsim.api.core.v01.population.PopulationWriter;
import org.matsim.core.config.Config;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.population.PopulationUtils;
import org.matsim.core.population.io.PopulationReader;
import org.matsim.core.scenario.ScenarioUtils;
import org.matsim.core.utils.geometry.CoordUtils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;

public class AddSubpopulation {
	
	public static List<Map<String, String>> read(File file) throws JsonProcessingException, IOException {
	    List<Map<String, String>> response = new LinkedList<Map<String, String>>();
	    CsvMapper mapper = new CsvMapper();
	    CsvSchema schema = CsvSchema.emptySchema().withHeader();
	    MappingIterator<Map<String,String>> it = mapper.readerFor(Map.class)
	    		   .with(schema)
	    		   .readValues(file);
	    while (it.hasNext()) {
	        response.add(it.next());
	    }
	    return response;
	}
	
public static void main(String[] args) {
		
		String configPath = "scenarios/sioux_falls_uam/uam_config.xml";
		String subpopsCsvPath = "scenarios/sioux_falls_uam/subpopulations/subpops_airport_zones.csv";
		String outputPopPath = "scenarios/sioux_falls_uam/population_spap.xml.gz";
		
		// load config and plans
		Config config = ConfigUtils.loadConfig(configPath);
		Scenario scenario = ScenarioUtils.loadScenario(config);
		Population population = scenario.getPopulation();
		Network network = scenario.getNetwork();
		
		// Read subpopulations from csv
		
		File csvFile = new File(subpopsCsvPath);
		List<Map<String, String>> subpopsList = null;
		try {
			subpopsList = read(csvFile);
		}
		catch(IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}
		
		Map<Id<Person>, ? extends Person> personsList = population.getPersons();
		for(Map<String, String> subpopMap : subpopsList) {
			Id<Person> personId = Id.createPersonId(subpopMap.get("person_id"));
			PopulationUtils.putSubpopulation(personsList.get(personId), subpopMap.get("subpop"));
		}
		

		new PopulationWriter(population,network).write(outputPopPath);
	}
}
