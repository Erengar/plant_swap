# Plant Swap
### Description
This web application was made in an effort to learn django and technologies used in front-end development, such as HTML, CSS and Javascript.   
You can think about this application as a public display place for collectors, which also allows exchange of items. Users can post their plants on website. This posting does not yet mean user is seeking trade. Plant is there just to be seen and potentialy liked by other people. When the user decides to sell a plant he can set it up for a sale. When he does so, other users are able to offer him trades for a given plant. The only officialy supported exchanged is between one plant for another plant. Once the offer is created receiver can either accept or decline. If it is accepted, trade goes into its second stage in which it is up to users to meet and exchange their plants. Users can provide location information for a given plant so it is possible for trade to even take place. Messaging system is also in place to facilitate conversation between exchangers. Each user then has to confirm that trade was carried out. Once both confirmations are in, plants change their owners with all content that is associated with them including likes it received before.  
### Technical
This website uses primarly technologies that are already included in django framework. That means it is primarly SSR web application that uses djangos template engine. Djangos ORM was also utilized extensively. Other prominent django technologies were django forms. Some automated testing was also done using djangos own unittests but also *selenium*. For CSS *[Bulma framework](https://bulma.io/)* was used. Javascript was primarly utilized to create *carousel* for images in plant view. But there are also other usecases such as *thumbnail selection*. You can also find some Ajax done with *Jquery*. Specifically *specie search* on front page, *like system*, *plant dropdown* in trade and *trade finalization*.  
You can visit website online at [this address](https://plant-swap.onrender.com). To see most of websites features it is recommended to login. You can create your account manually or using github. You can also login using this dummy account:  
*User name: Polo*   
*Password: Liteon987*   
If you wish to seed database to better see workings of pagination or ordering you can navigate to *Profile => Seed Plants*. This will spawn 1000 imageless plants under *Polo* account.   

To run website locally you need [poetry](https://python-poetry.org/) dependencies manager. Then in root of the application run following command to install all dependencies:  
`poetry install`  
After that you can run local server with:  
`poetry run python manage.py runserver`  
Locally you can login using same credentials. Database seeding works the same way.   

If you have all python dependencies(will be listed below or see pyproject.toml with required versions) you can run project using:  
`python manage.py runserver`

### Dependencies
django  
social-auth-app-django  
whitenoise  
pillow  
selenium 
psycopg2-binary  
gunicorn  
redis  
hiredis     
jquery  
htmx  
