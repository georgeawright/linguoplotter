var fs = require('fs');
var mathjs = require('mathjs');

exports.run = function(query) {
    try {
	stats = JSON.parse(fs.readFileSync("logs/stats.txt"));
    } catch (err) {
	stats = {};
    }
    hyperparams_programs_results = {};
    directories = [];
    fs.readdirSync('logs/').forEach(directory => {
	if (directory == "stats.txt" || directory == "stats1.txt" || directory ==  "texts.csv") {
	    return;
	}
	directories.push(directory);
	details_file = `logs/${directory}/details.txt`;
	details = JSON.parse(fs.readFileSync(details_file));
	hyperparams_name = details["hyper_parameters"];
	if (!(hyperparams_name in hyperparams_programs_results)) {
	    hyperparams_programs_results[hyperparams_name] = {};
	}
	program_name = details["Program"];
	if (!(program_name in hyperparams_programs_results[hyperparams_name])) {
	    hyperparams_programs_results[hyperparams_name][program_name] = [];
	}
	hyperparams_programs_results[hyperparams_name][program_name].push({
	    "output": details["result"],
	    "satisfaction": details["satisfaction"],
	    "codelets_run": details["codelets_run"],
	    "seed": details["random_seed"],
	});
    });
    hyperparams_programs_table = {};
    Object.keys(hyperparams_programs_results).forEach(hyperparams => {
	hyperparams_programs_table[hyperparams] = {};
	Object.keys(hyperparams_programs_results[hyperparams]).forEach(program => {
	    program_results = hyperparams_programs_results[hyperparams][program];
	    satisfactions = [];
	    non_null_satisfactions = [];
	    run_lengths = [];
	    null_count = 0;
	    program_results.forEach(result => {
		if (result["satisfaction"] === undefined) {
		    return;
		}
		satisfactions.push(result["satisfaction"]);
		run_lengths.push(result["codelets_run"]);
		if (result["output"] === null) {
		    null_count += 1;
		} else {
		    non_null_satisfactions.push(result["satisfaction"])
		}
	    });
	    hyperparams_programs_table[hyperparams][program] = {
		"mean_satisfaction": mathjs.mean(satisfactions),
		"median_satisfaction": mathjs.median(satisfactions),
		"max_satisfaction": mathjs.max(satisfactions),
		"mean_run_length": mathjs.mean(run_lengths),
		"median_run_length": mathjs.median(run_lengths),
		"timeout_rate": null_count / satisfactions.length,
		"non_null_satisfaction": non_null_satisfactions,
	    };
	});
    });
    hyperparams_table = {};
    doc = '';
    Object.keys(hyperparams_programs_table).forEach(hyperparams => {
	mean_satisfactions = [];
	median_satisfactions = [];
	max_satisfactions = [];
	mean_run_lengths = [];
	median_run_lengths = [];
	timeout_rates = [];
	non_null_satisfactions = [];
	Object.keys(hyperparams_programs_table[hyperparams]).forEach(program => {
	    p = hyperparams_programs_table[hyperparams][program];
	    mean_satisfactions.push(p["mean_satisfaction"]);
	    median_satisfactions.push(p["median_satisfaction"]);
	    max_satisfactions.push(p["max_satisfaction"]);
	    mean_run_lengths.push(p["mean_run_length"]);
	    median_run_lengths.push(p["median_run_length"]);
	    timeout_rates.push(p["timeout_rate"]);
	    non_null_satisfactions = non_null_satisfactions.concat(p["non_null_satisfaction"]);
	});
	console.log(hyperparams);
	console.log(non_null_satisfactions)
	hyperparams_table[hyperparams] = {
	    "mean_satisfaction": mathjs.mean(mean_satisfactions),
	    "median_satisfaction": mathjs.median(median_satisfactions),
	    "mean_max_satisfaction": mathjs.mean(max_satisfactions),
	    "median_max_satisfaction": mathjs.median(max_satisfactions),
	    "mean_run_length": mathjs.mean(mean_run_lengths),
	    "median_run_length": mathjs.median(median_run_lengths),
	    "mean_timeout_rate": mathjs.mean(timeout_rates),
	    "median_timeout_rate": mathjs.median(timeout_rates),
	    "mean_non_null_satisfaction": mathjs.mean(non_null_satisfactions),
	    "median_non_null_satisfaction": mathjs.median(non_null_satisfactions),
	}
	mean_satisfaction = hyperparams_table[hyperparams]["mean_satisfaction"];
	median_satisfaction = hyperparams_table[hyperparams]["median_satisfaction"];
	mean_max_satisfaction = hyperparams_table[hyperparams]["mean_max_satisfaction"];
	median_max_satisfaction = hyperparams_table[hyperparams]["median_max_satisfaction"];
	mean_run_length = hyperparams_table[hyperparams]["mean_run_length"];
	median_run_length = hyperparams_table[hyperparams]["median_run_length"];
	mean_timeout_rate = hyperparams_table[hyperparams]["mean_timeout_rate"];
	median_timeout_rate = hyperparams_table[hyperparams]["median_timeout_rate"];
	mean_non_null_satisfaction = hyperparams_table[hyperparams]["mean_non_null_satisfaction"];
	median_non_null_satisfaction = hyperparams_table[hyperparams]["median_non_null_satisfaction"];
	doc += `${hyperparams}\t${mean_satisfaction}\t${median_satisfaction}\t${mean_max_satisfaction}\t${median_max_satisfaction}\t${mean_run_length}\t${median_run_length}\t${mean_timeout_rate}\t${median_timeout_rate}\t${mean_non_null_satisfaction}\t${median_non_null_satisfaction}\n`;
    });
    return doc;
}
								     
