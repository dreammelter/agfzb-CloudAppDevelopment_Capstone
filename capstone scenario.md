A national car dealership with local branches spread across the United States recently conducted a market survey. One of the suggestions that emerged from the survey was that customers would find it beneficial if they could access a central database of dealership reviews across the country.

You are a new hire at the company. You are assigned the task of building a website that allows new and existing customers to look up different branches by state and look at customer reviews of the various branches. Customers should be able to create an account and add their review for any of the branches. The management hopes this will bring transparency to the system and also increase the trust customers have in the dealership.

After thorough research and brainstorming, the team developed use cases for anonymous, authorized, and admin users.

**Use cases for anonymous users:**
> 1.	View the "Contact Us" page.
> 2.	View the "About Us" page.
> 3.	View the list of dealerships.
> 4.	Filter the list of dealerships by state.
> 5.	Click on a dealership to view the reviews for that dealership on the details page.
> 6.	Log in using their credentials.

**Use cases for authorized users:** 
In addition to the above, *authorized users* should be able to write a review for any dealership on the dealership's page. In order to enable authorized users to write their reviews:
> 1.	A Review button should be provided against each dealer listed in the dealership table.
> 2.	Clicking on the Review button should take the user to the review page.
> 3.	Filling the form on the review page and submitting it should add the review. 
> ```python
> { "user_id": 1, 
> "name": "Berkly Shepley", => from Django "dealership": 15, => from the form "review": "Total grid-enabled service-desk", => form textbox "time": "", => current time "purchase": true, => form checkbox "purchase_date": "07/11/2020", => form calendar (bootstrap) "car_make": "Audi", => from django dropdown "car_model": "A6", => from django dropdown "car_year": 2010 => form django dropdown } 
> 
> ```
> 4.	On submission, user should be taken back to the dealership detail page with the submitted review featured at the top of the reviews list, sorted on time.
Use cases for admin users:
> 5.	Log in to the admin site with a predefined username and password.
> 6.	Add new make, model, and other attributes.

Your organization has assigned you as the Lead Cloud Application Developer on this project. Your job is to develop this portal as part of your Capstone project by following best practices for cloud application development.