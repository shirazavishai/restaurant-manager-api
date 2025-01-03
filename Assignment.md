Develop a simple system, that manages a list of restaurants and their properties. e.g. address, style (Italian, French, Korean), vegetarian (yes/no), opening hours, deliveries, etc.

The system will have an API for querying with a subset of these parameters and return a recommendation for a restaurant that answers the criteria,
including the time of the request to check if its open.

e.g. “A vegetarian Italian restaurant that is open now” this should return a Json object with the restaurant and all its properties:

```
{

    restaurantRecommendation :

    {

        name: ‘Pizza hut’,

        style: ‘Italian’,

        address: ‘wherever street 99, somewhere’,

        openHour: 09:00,

        clouseHour: 23:00,

        vegetarian : yes

    }

}
```

Requirements

1. The assignment submission should be done in a GIT repo that we can access, could be yours or a dedicated one.
    a. Please include all code required to set up the system .
2. The system has to be cloud-native, with a preference for Azure with a simple architecture that will require a minimal amount of maintenance.
3. The system should be written in full IaC style, I should be able to fully deploy it on my own cloud instance without making manual changes. Use Terraform for configuring the required cloud resources.
4. There should be some backend storage mechanism that holds the history of all requests and returned responses.
    a. Consider that the backend data stored is highly confidential.
5. Make sure the system is secure.
    a. However, there is no need for the user to authenticate with the system (Assume it’s a free public service)
6. The system code should be deployed using an automatic CI\CD pipeline following any code change, including when adding or updating restaurants.
7. The code should be ready for code review (as possible)
8. Coding: Python \ PowerShell 