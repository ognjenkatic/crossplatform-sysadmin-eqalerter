# EqAlerter

This application is used to create configurable alerts based on specific elasticsearch queries using the api. The app is meant to be periodically ran via some sort of scheduling mechanism.

## Code Structure

The application is split up into the following modules based on functionality:

* eqalerter - the high level logic of the application, initiates loading of configuration, querying, parsing, writing to disk and sending results.
* eqconfig - the application configuration, this is where the user defines values such as the alter sender email address, password, etc.
* eqdebug - handles debuging in a simple way, based on the verbocity setting it outputs only warnings or informational data aswell.
* eqquery - handles the crafting of elasticsearch queries and sending requests.
* eqparse - handles the parsing of elasticsearch results according to configuration specifications.
* eqsend - handles sending the emails to recipients.
* eqwrite - handles writing data to disk.
** Support for more than one index.

## Configuration

In order for minimise the code and avoid hard coding specific queries into the application itself, an alert specific configuration file is used. The user is free to create as many of such configuration files as desired and name them any way he likes. Configuration files must obey a simple structure:

<pre>
{
	"data_dict" : {
		"hostname"	:	"_source/agent/hostname",
		"process"	:	"_source/process/name",
		"source_ip"	:	"_source/source/ip",
		"method"	:	"_source/system/auth/ssh/method",
		"event"		:	"_source/system/auth/ssh/event",
		"user"		:	"_source/user/name",
		"timestamp"	:	"_source/@timestamp"
	},
	"index_name" : "My_index_name",
	"content" : "My email body content.",
	"subject" : "My email subject",
	"recipients" : ["example_recipient@example.org"],
	"alert_level" : "HIGH",
	"query" :{
	  "version": true,
	  "size": 500,
	  "sort": [
		{
		  "@timestamp": {
			"order": "desc",
			"unmapped_type": "boolean"
		  }
		}
	  ],
	  "_source": {
		"excludes": []
	  },
	  "query": {
      "bool": {
        "must": [
        {
          "range": {
          "@timestamp": {
            "format": "strict_date_optional_time",
            "gte": "now-2d/d",
            "lte": "now/d"
            ...

</pre>

These config keys have the following purposes:

* data_dict - the dictionary that maps data fields to be extracted from elasticsearch query responses and their path down the response json tree.
* index_name - the name of the index that is being queried.
* content - the text content of the mail being sent.
* subject - the subject of the mail being sent.
* recipients - the recipients of the email.
* alert_level - **currently not in use**.
* query - the json form of the elasticsearch query, these can be copy-pasted over from kibana by inspecting build queries.

The app is meant to be executed periodically as a cron task or by some other mechanism. Its frequency of execution should match the query time range. For example the app could be ran every 5m with the time range of:

<pre>
"gte": "now-5m/m",
"lte": "now/m"
</pre>

and with a query that checks for ssh events for a specific host whos logs are being shipped to elasticsearch. A setup like this would alert specified recipients of ssh activity.

## Usage

Example of usage:

<pre>
python3 eqalerter.py ssh_config1 -v
python3 eqalerter.py apache_errors
....
</pre>

The script has one mandatory and one optional argument, the mandatory argument specifies the name of the config file located in /configs and the optional argument -v makes the app be more verbose for debugging or logging purposes.

