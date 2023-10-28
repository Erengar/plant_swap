# Plant Swap
### Description
This web application was made in an effort to learn django and technologies used in front-end development, such as HTML, CSS and Javascript.   
Conceptualy this application is combination of some light social media aspects with market-place. You can think about it  as a public display place for collectors. Users can post their plants on website. This posting does not yet mean users is seeking trade, plant is just there to be seen and potentialy liked by other people. When the user decides to sell a plant he can set it up for a sale. When he does so other users are able to offer him trades for a given plant. The only officialy supported exchanged is between one plant for another plant. Once the offer is created receiver can either accept or decline. If it is accepted trade goes into its second stage in which it is up to users to meet and exchange a plant. Users can provide location information for a given plant so it is possible for trade to even take place. Messaging system is also in place to facilitate conversation between exchangers. Each user then has to confirm that trade was carried out. Once both confirmations are in, plants change their owners with all content that is associated with them including likes it received before.  
### Technical
This website users primarly technologies that are already included in django framework. That means it is primarly SSR web application that uses djangos template engine. Djangos ORM was also utilized extensively. Other prominent django technologies were django forms that required some more fine-grained manipulation for which I used *django-widget-tweaks* library. Some automated testing was also done using primarly djangos own unittests but also *selenium*. For CSS [Bulma framework](https://bulma.io/) was used. Javascript was primarly utilized to create carousel for images in plant view. But there are also other usecases such as thumbnail selection. You can also find some Ajax done with Jquery. Specifically *specie search* on front page, *like system*, *plant dropdown* in trade and *trade finalization*. 
To run website locally:  
`python manage.py runserver`

### Dependencies
django  
django-widget-tweaks  
social-app-django  
whitenoise  
pillow  
selenium  
jquery  
htmx  
