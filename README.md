# Game-Shop
Full-stack website development project built by integrating PostgreSQL, Flask and Bootstrap

## Requirement
1. One AWS RDS PostgreSQL instance (where you host your database and upload your data)
2. Flask (back-end server)

## Running
Once you get all the installation set, inside the command window (terminal), at the same folder as where the flaskr is at, input:  
`set FLASK_APP=flaskr`  
`set FLASK_ENV=development`  
`flask run`  
You can see your website on http://127.0.0.1:5000/

## Features Implemented 
* **Game Information** - each game has it's own webpage which includes information such as producer, price, description and etc.
* **Game List** - a list at the homepage with at most 10 games shown in one page. user can click on the next page to continue to browse games. Initially it is ordered by alphabetic, and after the user has something in the wishlist or has bought some games, the content of the game list will vary according to the game type the user has an interest. 
* **Personal Account** - people can input account, password and email to register to be a member. After login, the content of navigation bar changes from "register/login" to "transaction history/wishlist/logout".
* **Wishlist** - customer can add/remove game to their wishlist on the game introduction page, user can see what games are in the wishlist right now and can navigate to these games' introduction page if they changed their mind. 
* **Checkout** - a function exists under wishlist webpage when there's at least one game inside the wishlist. Customer can choose one from several payments (credit, cash, ...) to complete the transaction. After the process is done, the transaction record will show up at the transaction history page with the time shows when the transaction was made.  
* **Transaction History** - the page that lists your transaction record chronologically. User can access to one transaction to see the detail by click on the transaction ID.
* **Transaction Record** - contain transaction detail includes prices, time, games bought
* **Top 10 Sold Games** - we list the top 10 sold games based on real-time data, once people buy games, it will actually affect the rank

## Demonstration
![DEMO](https://github.com/Jefflin413/Game-Shop/blob/master/pictures/game%20shop.gif "DEMO.gif")  
More pictures can be seen in [pictures](https://github.com/Jefflin413/Game-Shop/tree/master/pictures "pictures")

## Enity, relation and constraint design behind the database 
### **ER-diagram**  
![ERdiagram](https://github.com/Jefflin413/Game-Shop/blob/master/pictures/ER-Diagram%203.png "ERdiagram.png")  


### **Description of entities, attributes and relationship sets**  
**PLAYER**: user of the website.  
　account: unique id that every player should have one.  
　email: unique email address and cannot be null. It is a candidate key.  
　name: player’s preferred name.  
　age: the age of player, which must be between 0 and 150.  
　country: the country player lives in, which can only be one country. The games content may be different based on location.  

**TRANSACTION**: an order that records transaction time, amount and payment.  
　tid: the unique identification number of a transaction entity.  
　price: how much money is involved in this transaction, which must be >= 0 (free games are possible).  
　date: the time of when transaction validated.  
　payment: the way that player used to pay for the merchandise.  

**GAME**: PC game.    
　gname: name of the game.  
　description: context about game content.  
　genre: the type of the game, can only be one.  
　price: how much does it cost to buy this game, which must be >= 0 (free games are possible).  
　date: the time when the game was published. Could be in the future.  

**PRODUCER**: the person who takes responsibility for the production of game.  
　pname: producer’s name.  
　nation: the nationality of the producer, which can only be one, if there are multiple nationalities, we will pick the country he mostly works in.  
　age: the age of the producer, which must be between 0 and 150.  

**COMPOSER**: the person who make music for the game.  
　cname: name of the composer.

**MUSIC_GENRE**: the type of music  
　mgenre: types of music.
	
**INSTRUMENT**: the instrument   
　iname: the name of the instrument


**DEVELOPER**: a company that makes games.  
　dname: name of the company.  
　started: the time when the company was founded.  
　location: which city the headquarter of the company is.  

**ATTEND**: a relationship set that describes which PLAYER attend in which TRANSACTION, and a TRANSACTION must be attended by exactly one PLAYER.  

**CONTAIN**: a relationship set that describes which GAME is contained in a pair of PLAYER and TRANSACTION, one PLAYER and TRANSACTION pair must at least has one game involved.  

**WISH_LIST**: place into which PLAYER can put games they are interested in.  

**KEY_PEOPLE**: representative that a DEVELOPER can have.  

**NOTABLE_WORKS**: representative works that a PRODUCER can have.  

**PRODUCE**: DEVELOPER produce GAME, and a GAME is produced by at least one DEVELOPER.  

**DUB**: COMPOSER makes music for GAME.  

**CAN_PLAY**: the INSTRUMENT the COMPOSER can play, and a composer must be able to play at least one instrument  

**HAS_PERFORMED**: the MUSIC_GENRE the COMPOSER has performed, and a composer must have performed at least one instrument  



