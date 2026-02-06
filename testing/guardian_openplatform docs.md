Overview

This overview will give you some idea of what data is available, how to find what you need, and what you will see when you make a request to us.

To access the API, you will need to sign up for an API key, which should be sent with every request. Plus, once we have your contact details we will be able to give you notice of any upcoming changes.

The easiest way to see what data is included is to explore the data. You can build complex queries quickly and browse the results.

If your application needs to regularly poll the API for updated content, there are a few things you should know. Please ensure that you read the guide for polling applications below before starting.

Endpoints

We provide several endpoints to retrieve different items:

Content
Tags
Sections
Editions
Single item
For each endpoint:

results can be filtered using parameters
response contains minimal detail by default but more data can be exposed using parameters
results are returned as paginated list of containing, by default, 10 entries per page
Paging Through Results

Results are returned as a paginated list, with a default of 10 results. In order to page through the results, you can add the page keyword to your query.

Example: https://content.guardianapis.com/search?page=2&q=debate&api-key=test

Content

The content endpoint (/search) returns all pieces of content in the API. For example, let's see if the Guardian has any content on political debates:

https://content.guardianapis.com/search?q=debates

Here the q parameter filters the results to only those that include that search term. In this case, there are many results, so we might want to filter down the response to something more meaningful, specifically looking for political content published in 2014, for example:

https://content.guardianapis.com/search?q=debate&tag=politics/politics&from-date=2014-01-01&api-key=test

Query operators

The q parameter supports AND, OR and NOT operators. For example:

debate AND economy (https://content.guardianapis.com/search?q=debate%20AND%20economy&tag=politics/politics&from-date=2014-01-01&api-key=test) returns only content that contains both "debate" and "economy".

debate AND NOT immigration (https://content.guardianapis.com/search?q=debate%20AND%20NOT%20immigration&tag=politics/politics&from-date=2014-01-01&api-key=test) returns only content that contains "debate" but does not contain "immigration".

The AND operator has a higher precedence than OR, but you can use parentheses to override this behavior. For example:

debate AND (economy OR immigration OR education) (https://content.guardianapis.com/search?q=debate%20AND%20(economy%20OR%20immigration%20education)&tag=politics/politics&from-date=2014-01-01&api-key=test) returns only content that contains both "debate" and and at least one of the following "economy", "immigration", "education".

Note that OR is the default operator, so you can omit it if you like. debate AND (economy immigration education) will behave the same as the above query.

Filters operators

Some filters support AND, OR and NOT operators through a a specific syntax:

AND: ,
OR: |
NOT: -
Expressions can be grouped using ().

Phrase search

You can also use double quotes to search for exact phrases. For example:

"mitochondrial donation" (https://content.guardianapis.com/search?q="mitochondrial%20donation"&tag=politics/politics&from-date=2014-01-01&api-key=test) returns only content that contains the phrase "mitochondrial donation".

Tags

The tags endpoint (/tags) returns all tags in the API. All Guardian content is manually categorised using these tags, of which there are more than 50,000.

A tag is a piece of data that we use to categorise our content. We use many different tags so understanding what they mean is important, and with new ones being added all the time you'll want to make sure to keep up to date with the changes.

For example, this article contains many tags including:

environment/recycling
environment/plasticbags
environment/energyefficiency
You can use these tags in your own queries to find other content that has the same tags, for example environment/recycling, like this:

https://content.guardianapis.com/search?tag=environment/recycling&api-key=test

Or you can search for tags containing the term green in the tag itself.

Finally, tags have types:

keyword -- a word describing what this piece of content is about
series -- the name of a regularly produced content feature, such as podcasts or columns, eg. 'Band of the week'
contributor -- the author or authors of a content item
tone -- the intent of the content, such as feature or obituary
type -- the media type, such as article, poll, video, etc
blog -- the name of one of the Guardian's blogs
Sections

The sections endpoint(/sections) returns all sections in the API.

We use sections to logically group our content.

For example, this article contains one section, technology, and you will find that within our technology section, technologically-related content will be clustered such as items covering games, iPhone, Sony, Google and others.

Each section in sections endpoint response has its own id value, and you can see how this can be appended to either our website url (webUrl) to see the web representation, or the api url (apiUrl) to see the API's representation of that content.

If you request apiUrl value, the API would recognise them as single item requests for sections and respond with the content that we store for those sections.

Editions

The editions endpoint (/editions) returns all editions in the API.

Editions are the regionalised front pages of the Guardian site. At current we have editions for the United Kingdom, the United States, Australia and Europe.

Single item

The single item endpoint returns all the data we have for a given single item id. Here the term 'item' refers to either a piece of content, a tag, or a section. The item endpoint matches the paths on theguardian.com. So by replacing the domain theguardian.com with content.guardianapis.com you can see the data associated.

For example:

a piece of content: https://content.guardianapis.com/technology/2014/feb/18/doge-such-questions-very-answered
a tag; https://content.guardianapis.com/world/france
a section: https://content.guardianapis.com/lifeandstyle
The response contains minimal detail by default but more data can be exposed by passing parameters in your request. Many (though not all) of these parameters are shared with the Content endpoint.

Polling guide

The key that you are assigned is rate-limited and as such any applications that depend on making large numbers of requests on a polling basis are likely to exceed their daily quota and thus be prevented from making further requests until the next period begins.

If you require an elevated limit on requests-per-day or requests-per-second this may be possible to arrange. Please contact us to discuss the nature of your application and the requests you are intending to make.

HTTPS support

The Content API is also available over HTTPS at https://content.guardianapis.com/ you are encouraged to use this for example where you need to call the Content API on the client-side as part of a secure application.

Client libraries

We maintain and support officially only one client, the Scala client library.

However, clients for other languages have been created by the developer community and you can find these on github:

Golang github.com/guardian/gocapiclient
Haskell github.com/guardian/content-api-haskell-client
Java
(Antonio Matarrese) github.com/matarrese/content-api-the-guardian
(Omoniyi Omotoso) github.com/niyiomotoso/the-guardian-api-java-client
Javascript (Kalob Porter) github.com/PorterK/GuardianJSClient
PHP (Omoniyi Omotoso) github.com/niyiomotoso/the-guardian-api-php-client
Python (Prabhath Kiran) github.com/prabhath6/theguardian-api-python
Ruby (Tom ten Thij) github.com/tomtt/contentapi-ruby
Rust (Mario Savarese) github.com/MarSavar/aletheia

\*\* Content

Endpoint URL

https://content.guardianapis.com/search
Example response

{
"response": {
"status": "ok",
"userTier": "developer",
"total": 1,
"startIndex": 1,
"pageSize": 10,
"currentPage": 1,
"pages": 1,
"orderBy": "newest",
"results": [
{
"id": "world/2022/oct/21/russia-ukraine-war-latest-what-we-know-on-day-240-of-the-invasion",
"type": "article",
"sectionId": "world",
"sectionName": "World news",
"webPublicationDate": "2022-10-21T14:06:14Z",
"webTitle": "Russia-Ukraine war latest: what we know on day 240 of the invasion",
"webUrl": "https://www.theguardian.com/world/2022/oct/21/russia-ukraine-war-latest-what-we-know-on-day-240-of-the-invasion",
"apiUrl": "https://content.guardianapis.com/world/2022/oct/21/russia-ukraine-war-latest-what-we-know-on-day-240-of-the-invasion",
"isHosted": false,
"pillarId": "pillar/news",
"pillarName": "News"
}
]
}
}
Field Description Type
status The status of the response. It refers to the state of the API. Successful calls will receive an "ok" even if your query did not return any results String
total The number of results available for your search overall Integer
pageSize The number of items returned in this call Integer
currentPage The number of the page you are browsing Integer
pages The total amount of pages that are in this call Integer
orderBy The sort order used String
id The path to content String
sectionId The id of the section String
sectionName The name of the section String
webPublicationDate The combined date and time of publication Datetime
webUrl The URL of the html content String
apiUrl The URL of the raw content String
Parameters

Authentication parameters

Name Description Type Accepted values
api-key The API key used for the query String
Format parameters

Name Description Type Accepted values
format The format to return the results in String json | xml
Cross origin requests parameters

Name Description Type Accepted values
callback The javascript callback name to wrap the JSON response. Read HTTP Status Codes and APIs: how the Guardian's Content API does it for more details String e.g. foo
Query term

Name Description Type Accepted values
q Request content containing this free text. Supports AND, OR and NOT operators, and exact phrase queries using double quotes. String e.g. sausages, "pork sausages", sausages AND (mash OR chips), sausages AND NOT (saveloy OR battered)
query-fields Specify in which indexed fields query terms should be searched on String list e.g. body, body,thumbnail
Filters

Name Description Type Accepted values Boolean operators
section Return only content in those sections String e.g. football
reference Return only content with those references String e.g. isbn/9780718178949
reference-type Return only content with references of those types String e.g. isbn
tag Return only content with those tags String e.g. technology/apple
rights Return only content with those rights String syndicatable, subscription-databases
ids Return only content with those IDs String e.g. technology/2014/feb/17/flappy-bird-clones-apple-google
production-office Return only content from those production offices String e.g. aus
lang Return only content in those languages String ISO language codes, e.g. en, fr
star-rating Return only content with a given star rating Integer 1 to 5
Date options

Name Description Type Accepted values
from-date Return only content published on or after that date Date e.g. 2014-02-16
to-date Return only content published on or before that date Date e.g. 2014-02-17
Name Description Type Accepted values
use-date Changes which type of date is used to filter the results using from-date and to-date String See list below
published - The date the content has been last published - Default
first-publication - The date the content has been first published
newspaper-edition - The date the content appeared in print
last-modified - The date the content was last updated
Page options

Name Description Type Accepted values
page Return only the result set from a particular page Integer e.g. 5
page-size Modify the number of items displayed per page Integer 1 to 50
Ordering

Name Description Type Accepted values
order-by Returns results in the specified order String See list below
newest - Default in all other cases
oldest
relevance - Default where q parameter is specified
Name Description Type Accepted values
order-date Changes which type of date is used to order the results String See list below
published - The date the content appeared on the web - Default
newspaper-edition - The date the content appeared in print
last-modified - The date the content was last updated
Additional information

Name Description Type Accepted values
show-fields Add fields associated with the content String list See table below
Field Description Type
trailText String (HTML)
headline String (HTML)
showInRelatedContent Whether this content can appear in automatically generated Related Content String (boolean)
body String (HTML)
lastModified Datetime
hasStoryPackage Has related content selected by editors String (boolean)
score A relevance score based on the search query used String (float)
standfirst String (HTML)
shortUrl String
thumbnail String
wordcount String (Integer)
commentable String (Boolean)
isPremoderated Comments will be checked by a moderator prior to publication if true String (Boolean)
allowUgc May have associated User Generated Content. This typically means the content has an associated Guardian Witness assignment which can be accessed by querying show-references=witness-assignment String (Boolean)
byline String (HTML)
publication String
internalPageCode String
productionOffice String
shouldHideAdverts Adverts will not be displayed if true String (Boolean)
liveBloggingNow Content is currently live blogged if true String (Boolean)
commentCloseDate The date the comments have been closed Datetime
starRating String (Integer)
all Includes all the fields
Name Description Type Accepted values
show-tags Add associated metadata tags String list See list below
blog
contributor
keyword
newspaper-book
newspaper-book-section
publication
series
tone
type
all
Name Description Type Accepted values
show-section Add associated metadata section String (boolean) e.g. true
Name Description Type Accepted values
show-blocks Add associated blocks (single block for content, one or more for liveblogs) String list See list below
main
body
all
body:latest
body:latest (limit defaults to 20)
body:latest:10
body:oldest
body:oldest:10
body:<block ID> (only the block with that ID)
body:around:<block ID> (the specified block and 20 blocks either side of it)
body:around:<block ID>:10 (the specified block and 10 blocks either side of it)
body:key-events
body:published-since:1556529318000 (only blocks since given timestamp)
Name Description Type Accepted values
show-elements Add associated media elements such as images and audio String list See list below
audio
image
video
all
Name Description Type Accepted values
show-references Add associated reference data such as ISBNs String list See list below
author
bisac-prefix
esa-cricket-match
esa-football-match
esa-football-team
esa-football-tournament
isbn
imdb
musicbrainz
musicbrainzgenre
opta-cricket-match
opta-football-match
opta-football-team
opta-football-tournament
pa-football-competition
pa-football-match
pa-football-team
r1-film
reuters-index-ric
reuters-stock-ric
witness-assignment - See allowUgc
Name Description Type Accepted values
show-rights Add associated rights String list See list below
syndicatable
subscription-databases
all
Example query

https://content.guardianapis.com/search?q=12%20years%20a%20slave&format=json&tag=film/film,tone/reviews&from-date=2010-01-01&show-tags=contributor&show-fields=starRating,headline,thumbnail,short-url&show-refinements=all&order-by=relevance

Deep pagination

Page options (above) allow you to paginate through several thousand results using page and pageSize. There is a limit to how deep you can go using this approach.

If your application needs to paginate beyond these limits you will need to use the content /next end point rather than page options.

Using the content /next end point

Start your search using the /search end point.

ie. https://content.guardianapis.com/search?q=sausages&page-size-10&order-by=relevance

{
"response": {
"status": "ok",
"total": 5857,
"startIndex": 1,
"pageSize": 10,
"currentPage": 1,
"pages": 586,
"orderBy": "relevance",
"results": [
{
"id": "food/2023/mar/22/how-to-make-glamorgan-sausages-recipe-felicity-cloake",
"type": "article",
"sectionId": "food",
"sectionName": "Food",
"webPublicationDate": "2023-03-22T12:00:26Z",
"webTitle": "How to make Glamorgan sausages | Felicity Cloake's Masterclas",
"webUrl": "https://www.theguardian.com/food/2023/mar/22/how-to-make-glamorgan-sausages-recipe-felicity-cloake",
"apiUrl": "https://content.guardianapis.com/food/2023/mar/22/how-to-make-glamorgan-sausages-recipe-felicity-cloake",
"isHosted": false,
"pillarId": "pillar/lifestyle",
"pillarName": "Lifestyle"
},
... 8 results omitted ...
{
"id": "food/2022/jul/04/peperonata-sausages-recipe-rachel-roddy",
"type": "article",
"sectionId": "food",
"sectionName": "Food",
"webPublicationDate": "2022-07-04T10:00:40Z",
"webTitle": "Rachel Roddy’s recipe for peperonata with sausages | A kitchen in Rome",
"webUrl": "https://www.theguardian.com/food/2022/jul/04/peperonata-sausages-recipe-rachel-roddy",
"apiUrl": "https://content.guardianapis.com/food/2022/jul/04/peperonata-sausages-recipe-rachel-roddy",
"isHosted": false,
"pillarId": "pillar/lifestyle",
"pillarName": "Lifestyle"
}
]
}
}
Note the total, pages and currentPage values. These show you that there are more results than what is shown on the current page.

Take the id of the last result. It is food/2022/jul/04/peperonata-sausages-recipe-rachel-roddy in this example.

We can continue our pagination using the /next end point for this content item.

Preserving your query parameters and ordering, call the content /next end point for the last piece of content seen:

ie. https://content.guardianapis.com/content/food/2022/jul/04/peperonata-sausages-recipe-rachel-roddy/next?q=sausages&page-size=10&order-by=relevance

{
"response": {
"status": "ok",
"total": 5857,
"startIndex": 1,
"pageSize": 10,
"currentPage": 1,
"pages": 586,
"orderBy": "relevance",
"results": [
... 9 results omitted ...
{
"id": "commentisfree/2022/jun/20/big-festivals-glastonbury-so-white-lenny-henry-lack-of-diversity-arts-culture",
"type": "article",
"sectionId": "commentisfree",
"sectionName": "Opinion",
"webPublicationDate": "2022-06-20T14:00:17Z",
"webTitle": "Why are big festivals like Glastonbury so white? | Stephanie Phillips",
"webUrl": "https://www.theguardian.com/commentisfree/2022/jun/20/big-festivals-glastonbury-so-white-lenny-henry-lack-of-diversity-arts-culture",
"apiUrl": "https://content.guardianapis.com/commentisfree/2022/jun/20/big-festivals-glastonbury-so-white-lenny-henry-lack-of-diversity-arts-culture",
"isHosted": false,
"pillarId": "pillar/opinion",
"pillarName": "Opinion"
}
]
}
}
Take the id of the last result and repeat:

ie. https://content.guardianapis.com/content/commentisfree/2022/jun/20/big-festivals-glastonbury-so-white-lenny-henry-lack-of-diversity-arts-culture/next?q=sausages&page-size=10&order-by=relevance

Continue iterating using the id of the last result seen. Eventually you will receive a response containing fewer results than the page size.

ie. https://content.guardianapis.com/content/film/1998/mar/23/features/next?q=sausages&page-size=10&order-by=relevance

{
"response": {
"status": "ok",
"total": 5857,
"startIndex": 1,
"pageSize": 10,
"currentPage": 1,
"pages": 586,
"orderBy": "relevance",
"results": [
... 2 results ommitted ...
{...},
{...}
]
}
}
This indicates that you have reached the end and can stop querying.

\*\* Tags

Endpoint URL

http://content.guardianapis.com/tags
Example response

{
"response": {
"status": "ok",
"userTier": "developer",
"total": 65,
"startIndex": 1,
"pageSize": 10,
"currentPage": 1,
"pages": 7,
"results": [
{
"id": "katine/football",
"type": "keyword",
"webTitle": "Football",
"webUrl": "http://www.theguardian.com/katine/football",
"apiUrl": "http://beta.content.guardianapis.com/katine/football",
"sectionId": "katine",
"sectionName": "Katine"
}
]
}
}
Field Description Type
status The status of the response. It refers to the state of the API. Successful calls will receive an "ok" even if your query did not return any results String
total The number of results available for your search overall Integer
startIndex ? Integer
pageSize The number of items returned in this call Integer
currentPage The number of the page you are browsing Integer
pages The total amount of pages that are in this call Integer
id The id of the tag String
type The type of the tag String
webUrl The URL of the html content String
apiUrl The URL of the raw content String
sectionId The id of the section String
sectionName The name of the section String
Parameters

Authentication parameters

Name Description Type Accepted values
api-key The API key used for the query String
Format parameters

Name Description Type Accepted values
format The format to return the results in String json | xml
Cross origin requests parameters

Name Description Type Accepted values
callback The javascript callback name to wrap the JSON response. Read HTTP Status Codes and APIs: how the Guardian's Content API does it for more details String e.g. foo
Query term

Name Description Type Accepted values
q Request tags containing exactly this free text String e.g. sausages
web-title Request tags starting with this free text String e.g. sausa
Filters

Name Description Type Accepted values Boolean operators
type Return only tags of that type String
section Return only tags in those sections String e.g. football
reference Return only tags with those references String e.g. isbn/9780349108391
reference-type Return only tags with references of those types String e.g. isbn
Page options

Name Description Type Accepted values
page Returns results only for that page index Integer e.g. 5
page-size Modify the number of items displayed per page Integer Default: 10
Additional information

Name Description Type Accepted values
show-references Show associated reference data such as ISBNs String list See list below
author
bisac-prefix
esa-cricket-match
esa-football-match
esa-football-team
esa-football-tournament
isbn
imdb
musicbrainz
musicbrainzgenre
opta-cricket-match
opta-football-match
opta-football-team
opta-football-tournament
pa-football-competition
pa-football-match
pa-football-team
r1-film
reuters-index-ric
reuters-stock-ric
witness-assignment
Example

http://content.guardianapis.com/tags?q=apple&section=technology&show-references=all

\*\* Sections

Endpoint URL

https://content.guardianapis.com/sections
Example response

{
"response": {
"status": "ok",
"userTier": "developer",
"total": 1,
"results": [
{
"id": "football",
"webTitle": "Football",
"webUrl": "https://www.theguardian.com/football",
"apiUrl": "https://content.guardianapis.com/football",
"editions": [
{
"id": "football",
"webTitle": "Football",
"webUrl": "https://www.theguardian.com/football",
"apiUrl": "https://content.guardianapis.com/football",
"code": "default"
}
]
}
]
}
}
Field Description Type
status The status of the response. It refers to the state of the API. Successful calls will receive an "ok" even if your query did not return any results String
total The number of results available for your search overall Integer
id The id of the section String
webTitle The title displayed on the web String
webUrl The URL of the html content String
apiUrl The URL of the raw content String
editions The list of existing editions for this section String
code The code of the edition String
Parameters

Authentication parameters

Name Description Type Accepted values
api-key The API key used for the query String
Format parameters

Name Description Type Accepted values
format The format to return the results in String json | xml
Cross origin requests parameters

Name Description Type Accepted values
callback The javascript callback name to wrap the JSON response. Read HTTP Status Codes and APIs: how the Guardian's Content API does it for more details String e.g. foo
Query term

Name Description Type Accepted values
q Return section based on the query term specified String e.g. business
Example

https://content.guardianapis.com/sections?q=business&api-key=test

\*\* Editions

Endpoint URL

https://content.guardianapis.com/editions
Example response

{
"response": {
"status": "ok",
"userTier": "developer",
"total": 5,
"results": [
{
"id": "au",
"path": "au",
"edition": "AU",
"webTitle": "new guardian australia front page",
"webUrl": "https://www.theguardian.com/au",
"apiUrl": "https://content.guardianapis.com/au"
},
{
"id": "europe",
"path": "europe",
"edition": "Europe",
"webTitle": "new guardian europe front page",
"webUrl": "https://www.theguardian.com/europe",
"apiUrl": "https://content.guardianapis.com/europe"
},
{
"id": "international",
"path": "international",
"edition": "International",
"webTitle": "new guardian international front page",
"webUrl": "https://www.theguardian.com/international",
"apiUrl": "https://content.guardianapis.com/international"
},
{
"id": "uk",
"path": "uk",
"edition": "UK",
"webTitle": "new guardian uk front page",
"webUrl": "https://www.theguardian.com/uk",
"apiUrl": "https://content.guardianapis.com/uk"
},
{
"id": "us",
"path": "us",
"edition": "US",
"webTitle": "new guardian us front page",
"webUrl": "https://www.theguardian.com/us",
"apiUrl": "https://content.guardianapis.com/us"
}
]
}
}
Field Description Type
status The status of the response. It refers to the state of the API. Successful calls will receive an "ok" even if your query did not return any results String
total The number of results available for your search overall Integer
id The id of the edition String
webTitle The title displayed on the web String
webUrl The URL of the html content String
apiUrl The URL of the raw content String
edition The edition name String
path The path of the edition String
Parameters

Authentication parameters

Name Description Type Accepted values
api-key The API key used for the query String
Format parameters

Name Description Type Accepted values
format The format to return the results in String json | xml
Cross origin requests parameters

Name Description Type Accepted values
callback The javascript callback name to wrap the JSON response. Read HTTP Status Codes and APIs: how the Guardian's Content API does it for more details String e.g. foo
Query term

Name Description Type Accepted values
q Return edition based on the query term specified String e.g. UK
Example

https://content.guardianapis.com/editions?q=uk&api-key=test

\*\* Single Item

Endpoint URL

https://content.guardianapis.com/
Example

Query

https://content.guardianapis.com/sport/2022/oct/07/cricket-jos-buttler-primed-for-england-comeback-while-phil-salt-stays-focused?api-key=test

Response

{
"response": {
"status": "ok",
"userTier": "developer",
"total": 1,
"content": {
"id": "sport/2022/oct/07/cricket-jos-buttler-primed-for-england-comeback-while-phil-salt-stays-focused",
"type": "article",
"sectionId": "sport",
"sectionName": "Sport",
"webPublicationDate": "2022-10-07T12:00:01Z",
"webTitle": "Jos Buttler primed for England comeback while Phil Salt stays focused",
"webUrl": "https://www.theguardian.com/sport/2022/oct/07/cricket-jos-buttler-primed-for-england-comeback-while-phil-salt-stays-focused",
"apiUrl": "https://content.guardianapis.com/sport/2022/oct/07/cricket-jos-buttler-primed-for-england-comeback-while-phil-salt-stays-focused",
"isHosted": false,
"pillarId": "pillar/sport",
"pillarName": "Sport"
}
}
}
Field Description Type
status The status of the response. It refers to the state of the API. Successful calls will receive an "ok" even if your query did not return any results String
total The number of results available for your search overall Integer
leadContent To help show which are the key pieces of content at any one time, editors identify those pieces of content as "lead" for the tag in question String - list of items
Parameters

Authentication parameters

Name Description Type Accepted values
api-key The API key used for the query String
Format parameters

Name Description Type Accepted values
format The format to return the results in String json | xml
Cross origin requests parameters

Name Description Type Accepted values
callback The javascript callback name to wrap the JSON response. Read HTTP Status Codes and APIs: how the Guardian's Content API does it for more details String e.g. foo
Query term

Field Description Type Accepted values
id The ID for an item, such as a piece of content, is the path to that item on the site. By replacing the domain with content.guardianapis.com you get the API URL for that piece of content String
Filters

Name Description Type Accepted values Boolean operators
section Return only content in those sections String e.g. football
reference Return only content with those references String e.g. isbn/9780718178949
reference-type Return only content with references of those types String e.g. isbn
tag Return only content with those tags String e.g. technology/apple
rights Return only content with those rights String syndicatable, subscription-databases
ids Return only content with those IDs String e.g. technology/2014/feb/17/flappy-bird-clones-apple-google
production-office Return only content from those production offices String e.g. aus
lang Return only content in those languages String ISO language codes, e.g. en, fr
star-rating Return only content with a given star rating Integer 1 to 5
Date options

Name Description Type Accepted values
from-date Return only content published on or after that date Date e.g. 2014-02-16
to-date Return only content published on or before that date Date e.g. 2014-02-17
Name Description Type Accepted values
use-date Changes which type of date is used to filter the results using from-date and to-date String See list below
published - The date the content has been last published - Default
first-publication - The date the content has been first published
newspaper-edition - The date the content appeared in print
last-modified - The date the content was last updated
Page options

Name Description Type Accepted values
page Return only the result set from a particular page Integer e.g. 5
page-size Modify the number of items displayed per page Integer 1 to 50
Ordering

Name Description Type Accepted values
order-by Returns results in the specified order String See list below
newest - Default in all other cases
oldest
relevance - Default where q parameter is specified
Name Description Type Accepted values
order-date Changes which type of date is used to order the results String See list below
published - The date the content appeared on the web - Default
newspaper-edition - The date the content appeared in print
last-modified - The date the content was last updated
Additional information

Name Description Type Accepted values
show-fields Add fields associated with the content String list See table below
Field Description Type
trailText String (HTML)
headline String (HTML)
showInRelatedContent Whether this content can appear in automatically generated Related Content String (boolean)
body String (HTML)
lastModified Datetime
hasStoryPackage Has related content selected by editors String (boolean)
score A relevance score based on the search query used String (float)
standfirst String (HTML)
shortUrl String
thumbnail String
wordcount String (Integer)
commentable String (Boolean)
isPremoderated Comments will be checked by a moderator prior to publication if true String (Boolean)
allowUgc May have associated User Generated Content. This typically means the content has an associated Guardian Witness assignment which can be accessed by querying show-references=witness-assignment String (Boolean)
byline String (HTML)
publication String
internalPageCode String
productionOffice String
shouldHideAdverts Adverts will not be displayed if true String (Boolean)
liveBloggingNow Content is currently live blogged if true String (Boolean)
commentCloseDate The date the comments have been closed Datetime
starRating String (Integer)
all Includes all the fields
Name Description Type Accepted values
show-tags Add associated metadata tags String list See list below
blog
contributor
keyword
newspaper-book
newspaper-book-section
publication
series
tone
type
all
Name Description Type Accepted values
show-section Add associated metadata section String (boolean) e.g. true
Name Description Type Accepted values
show-blocks Add associated blocks (single block for content, one or more for liveblogs) String list See list below
main
body
all
body:latest
body:latest (limit defaults to 20)
body:latest:10
body:oldest
body:oldest:10
body:<block ID> (only the block with that ID)
body:around:<block ID> (the specified block and 20 blocks either side of it)
body:around:<block ID>:10 (the specified block and 10 blocks either side of it)
body:key-events
body:published-since:1556529318000 (only blocks since given timestamp)
Name Description Type Accepted values
show-elements Add associated media elements such as images and audio String list See list below
audio
image
video
all
Name Description Type Accepted values
show-references Add associated reference data such as ISBNs String list See list below
author
bisac-prefix
esa-cricket-match
esa-football-match
esa-football-team
esa-football-tournament
isbn
imdb
musicbrainz
musicbrainzgenre
opta-cricket-match
opta-football-match
opta-football-team
opta-football-tournament
pa-football-competition
pa-football-match
pa-football-team
r1-film
reuters-index-ric
reuters-stock-ric
witness-assignment - See allowUgc
Name Description Type Accepted values
show-rights Add associated rights String list See list below
syndicatable
subscription-databases
all
Field Description Type Accepted values
show-story-package When true display a list of content that is in the has been identified as being about the same story as the requested content item. When a content item is in a package the hasStoryPackage field has a value of true Boolean true \
show-editors-picks When true display a list of content that is chosen by editors on tags, sections and the home page. This content list represents the main list of content found on the equivalent path on the site Boolean true \
show-most-viewed When true display most viewed content. For overall most viewed set id to '/', for section most viewed set id to the section id
show-related Content items can show a set of 'related' content. When true returns content items related to the main content item Boolean true \
