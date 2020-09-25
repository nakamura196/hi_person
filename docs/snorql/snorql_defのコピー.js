//snorql.js / snorql_ldb.js custom configuration
//@version 2020-06-01
var Snorqldef = {
	//overrides Snorql class variables
	vars: {
		//_endpoint: "/works/ld/jpsearch/ep",
		_endpoint: "https://diyhistory.org/c.php/http://3.91.74.60:8890/sparql",
		_poweredByLink: "https://www.hi.u-tokyo.ac.jp/publication/syoho/10/pub_kokiroku-minkeiki-01.html",
		_poweredByLabel: "民経記人物DB",
		default_query: "SELECT DISTINCT * WHERE {\n\t?s rdfs:label ?label . \n}\nORDER BY ?s\nLIMIT 100",
		link_img: "link.png",	//relative position 2019-01-20
		//prefixes to display properties as QName (in addtion to basic snorql._namespace)
		more_ns: {
			"dc": "http://purl.org/dc/elements/1.1/",
			"dct": "http://purl.org/dc/terms/"
		}
	},
	//home setting properties: this is for Japan Search
	home: {
    	label: "民経記人物DB",
		uri: "https://www.hi.u-tokyo.ac.jp/publication/syoho/10/pub_kokiroku-minkeiki-01.html",
		datauri: "https://jpsearch.go.jp/data/",	//basic 'record' namespace
		datauri_pat: "^(https://jpsearch.go.jp|https://ld.cultural.jp|http://purl.org/net/ld/jpsearch)/data/",	//basic 'record' namespace
		data_frags: ["accessinfo", "sourceinfo"],
		//workuri: ["https://jpsearch.go.jp/entity/work/"],	//additional 'record' namespaces
		workuri: ["https://jpsearch.go.jp/entity/", "https://jpsearch.go.jp/term/keyword/"],	//additional 'record' namespaces
		submit_selector: ".section input[type=button]",	//query selector for the button to replace label
		submit_label: ["クエリ実行", "Run Query"],	//display label for the submit button [ja, en]
      /*
      intro: [
			["用いているRDFモデルの概要は<a href=\"https://jpsearch.go.jp/api/introduction/\">利活用スキーマ概説</a>をご覧ください。", "See <a href=\"https://jpsearch.go.jp/api/introduction/\">Introduction to Japan Search SPARQL Endpoint</a> (in Japanese) for the RDF mode."],
			["<a href=\"/doc/about-sources.html\">取得ソース</a>や<a href=\"/doc/about-rdf.html\">RDF変換の制約</a>および<a href=\"/doc/license-description.html\">ライセンスのRDF表現</a>についての簡単な説明を用意しています。", "A short description of <a href=\"/doc/about-sources.html\">aggregation sources</a> and <a href=\"/doc/about-rdf.html\">some RDF limitations</a> and <a href=\"/doc/license-description.html\">license description in RDF</a> (in Japanese) available."],
      ]
      */
	},
	//snoral_ldb configuration
	ldb: {
		//special treatment properties
		//[pfx, localname] where pfx is defined in namespaces.js
		label_prop: ["rdfs", "label"],
		img_prop: ["schema", "associatedMedia"],
		thumb_prop: ["schema", "image"],	//maybe we should use schema:thumbnail
		geo: {
			prop: ["schema", "geo"],
			strctprop : ["jps", "spatial"],
			regionprop : ["jps", "region"],
			valprop : ["jps", "value"],
			locprop : ["schema", "location"]
		},
		//preferred order of properties. used in JsonRDFFormatter.
		proporder: {
			//the latter the heigher priority (top)
			showup: [
				["jps", "within"],
				["schema", "longitude"],
				["schema", "latitude"],
				["schema", "geo"],
				["jps", "value"],
				["jps", "relationType"],
				["schema", "datePublished"],
				["schema", "dateCreated"],
				["schema", "temporal"],
				["schema", "spatial"],
				["schema", "publisher"],
				["schema", "contributor"],
				["schema", "creator"],
				["schema", "name"],
				["dct", "http://purl.org/dc/terms/title"],
				["skosxl", "http://www.w3.org/2008/05/skos-xl#altLabel"],
				["skosxl", "http://www.w3.org/2008/05/skos-xl#prefLabel"],
				["rdfs", "label"],
				["rdf", "type"]
			],
			//the latter the lower priority (bottom)
			showdown: [
				["jps", "accessInfo"],
				["jps", "sourceInfo"]
			]
		},
		//propety based class attribute. used in JsonRDFFormatter
		propclass: {
			"rdf:type" : "type",
			"schema:publisher" : "agential",
			"schema:contributor" : "agential",
			"schema:creator" : "agential",
			"jps:agential" : "agential",
			"schema:datePublished" : "temporal",
			"schema:dateCreated" : "temporal",
			"schema:temporal" : "temporal",
			"jps:temporal" : "temporal",
			"schema:spatial" : "spatial",
			"jps:spatial" : "spatial"
		},
		//suffix mapping for external links. used in JsonRDFFormatter
		link_sfx: [{ns: "http://geohash.org/", sfx: "?format=osm"}],	//sfx: "?format=text"
		showrows: 6,	//default open rows for multiple values (e.g. schema:description)
		////// ★change setting for JPS
		use_iiif_viewer: true,
		//leaftet template information. used in Util.map.setup
		mapd: "openstreetmap.org",	//"maps.gsi.go.jp",
		maps: {
			"openstreetmap.org": {
				template: ["https://{s}.tile.osm.org/{z}/{x}/{y}.png",	//ja
					"https://{s}.tile.osm.org/{z}/{x}/{y}.png"],	//en
				aerial: "https://cyberjapandata.gsi.go.jp/xyz/ort/{z}/{x}/{y}.jpg",
				lp: "qparam",
				fillopc: 0.15,
				attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
			},
			"maps.gsi.go.jp": {
				template: ["https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png",	//ja
					"https://cyberjapandata.gsi.go.jp/xyz/english/{z}/{x}/{y}.png"],	//en
				aerial: "https://cyberjapandata.gsi.go.jp/xyz/ort/{z}/{x}/{y}.jpg",
				lp: "hash",
				fillopc: 0.28,
				attribution: '<a href="http://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html">国土地理院</a>'
			},
			"pale.maps.gsi.go.jp": {
				template: ["https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
					"https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png"],
				aerial: "https://cyberjapandata.gsi.go.jp/xyz/ort/{z}/{x}/{y}.jpg",
				lp: "hash",
				fillopc: 0.15,
				attribution: '<a href="http://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html">国土地理院</a>'
			}
		},
		texternal: [87,87,87,14,75,65,78,90,65,75,73,14,67,79,77]
	},
	//specify {endpoint: new RegExp(uri_pattern)} to link certain uris to different endpoint
	describer_map: null,
	qtemplate: {
		solslabel: "?label ?mtlabel",
		condlabel: "?label .\n\tOPTIONAL{$1 schema:name ?mtlabel FILTER(lang(?mtlabel)=\"ja-x-mt\")}\n\t$1"
	},
	//additional namespaces (not defined in namespaces.js) to use in examples
	example_ns: {
		"edm": "http://www.europeana.eu/schemas/edm/",
		"ore": "http://www.openarchives.org/ore/terms/",
		"wdt": "http://www.wikidata.org/prop/direct/",
		"crm": "http://www.cidoc-crm.org/cidoc-crm/",
		//"foaf"=>"http://xmlns.com/foaf/0.1/",
		"dc": "http://purl.org/dc/elements/1.1/"
	}
};

//Snorqldef.img_extra = function(opt, uri){
//	if(uri.match(/^https?:\/\/\w+\.britishmuseum\.org/)) opt.recover = "https://ld.cultural.jp/app/prx?u=" + uri;
//};
//property description, hierarchy
Snorqldef.prop_description = {
	"schema:image": ["アイテムの代表画像。主としてサムネイル。", "Item's representative image, namely a thumbnail."],
	"jps:accessInfo_g": {
		"schema:provider": ["アイテムの所蔵者、あるいはアイテムへのアクセスの提供者。", "The holder of, or access provider to the item."],
		"schema:associatedMedia": ["アイテムのデジタル化オブジェクト。主として画像。", "Item's digitized object, namely an image."],
		"schema:url": ["アイテムの紹介やアクセス情報が記載されたページ、もしくはファイル。", "Web page of the access or contents information, or related file."],
		"schema:relatedLink": ["コンテンツ一覧ページなど、コンテンツがその一部として取り上げられているページ。", "Link to resource(s) where the item is listed as a part of contents."]
	},
	"jps:sourceInfo_g": {
		"schema:provider": ["アイテムの元メタデータの提供者、もしくはデータベース。", "The provider of source metadata of the item."],
		"schema:url": ["ソース（元メタデータ）提供者のアイテム情報ページ。", "The item page of the source metadata provider."],
		"schema:relatedLink": [Snorqldef.home.label + "のアイテムページ。", "The item page of " + Snorqldef.home.label]
	}
};

//list of example queries. each object represents one example: {label: Japanese label for select option, label_en: English label for select option, ns: [prefixes to use in query], query: SPARQL query (escaped)}
Snorqldef.example = [
	
	{
		"label" : "天皇一覧",
		"label_en" : "天皇一覧",
		"ns" : [ ],
		"query" : "SELECT DISTINCT ?s ?start ?end ?image WHERE {\n	?s a type:Emperor.json;\n                      jps:start ?start;\n                      jps:end ?end . \n  optional {?s schema:image ?image}\n}\nORDER BY ?end\nLIMIT 100"
	},
	{
		"label" : "将軍一覧",
		"label_en" : "将軍一覧",
		"ns" : [ ],
		"query" : "SELECT DISTINCT ?s ?start ?end ?image WHERE {\n	?s a type:Shogunate.json;\n                      jps:start ?start;\n                      jps:end ?end . \n  optional {?s schema:image ?image}\n}\nORDER BY ?end\nLIMIT 100"
	},
	{
		"label" : "出来事一覧",
		"label_en" : "出来事一覧",
		"ns" : [ ],
		"query" : "SELECT DISTINCT ?s ?start ?end ?description WHERE {\n	?s a type:Time.json;\n                      jps:start ?start;\n                      jps:end ?end;\n                      schema:description ?description . \n}\nORDER BY ?end\nLIMIT 100"
	},
	{
		"label": "官位一覧",
		"label_en" : "官位一覧",
		"ns" : [ ],
		"query" : "SELECT DISTINCT ?s ?label WHERE {\n	?s a type:Kani.json;\n                   rdfs:label ?label.\n}\nLIMIT 100"
	},
	{
		"label": "人物一覧",
		"label_en" : "人物一覧",
		"ns" : [ ],
		"query" : "SELECT DISTINCT ?s ?label ?image WHERE {\n	?s a type:Person.json;\n                   rdfs:label ?label.\n  optional {?s schema:image ?image }\n}\nORDER BY desc(?image)\nLIMIT 100"
	},
	{
		"label": "藤原経光の経歴",
		"label_en" : "藤原経光の経歴",
		"ns" : [ ],
		"query" : "SELECT ?start ?end ?description ?value ?type WHERE {\n  graph ?g { \n    chname:藤原経光.json prop-ja:官位 ?o . \n    ?o schema:description ?description;\n       jps:start ?start . \n    optional { ?o jps:end ?end }\n    optional { ?o jps:relationType ?type }\n    optional { ?o jps:value ?value }\n  } \n} order by ?start"
	},
	{
		"label": "地名一覧",
		"label_en" : "地名一覧",
		"ns" : [ ],
		"query" : "SELECT DISTINCT ?s ?label WHERE {\n	graph ?g { ?s a type:Place.json;\n                    rdfs:label ?label . } \n}"
	},
	{
		"label": "位階一覧",
		"label_en" : "位階一覧",
		"ns" : [ ],
		"query" : "SELECT DISTINCT ?s ?label WHERE {\n	graph ?g { ?s a type:位階.json;\n                    rdfs:label ?label;\n             schema:position ?position .} \n} order by ?position"
	},
	{
		"label": "太政官一覧",
		"label_en" : "太政官一覧",
		"ns" : [ ],
		"query" : "SELECT DISTINCT ?s ?label ?ikai WHERE {\n	graph ?g { ?s a type:太政官.json;\n                    rdfs:label ?label;\n             schema:position ?position;\n                    skos:closeMatch ?ikai . } \n} order by ?position"
	},
];
