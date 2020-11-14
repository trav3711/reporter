#  To Do:

1. build database/gather data
    1. scrape data
        * create a Scraper class that can be applied to any news website
            - nytimes
            - ~economist~
            - WSJ
            - The intercept
            - Fox
            - Vox
        * every scraped article should be output as a txt file(maybe csv)
            - name date, author, content
        * use summarizer module to create a one sentence summary of each article
        * once a website is scraped, a JSON payload should be output
    3. create a lambda cluster so my requests don't get cut off
    2. convert to NoSQL MongoDB with JSON(I don't really know how this works)

2. deploy
    1. Create flask for backend
    2. Create simple Jinja template for front end
    3. Buy domain name

* Scraper class
    * attributes
        - BASE_URL
        - ENDPOINTS
        - master dictionary that becomes JSON output
        - list of tag,class tuples to grab content from
            1. tag, topics class
            2. tag, article title class
            3. tag, article author class
            4. tag, article date class
            5. tag, article body
            -
    * functions
        - get_endpoints
        - get_articles
        - write_to_file
