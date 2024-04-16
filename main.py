import Driver
import SQL
import SuitesList
import Components
import CleanData


input = input("Enter selection")

if input == '1':
    print("Check daily listings and update listings")
    Driver.run_through_the_types_of_listings_in_neighbourhoods(1, 3)
    #Driver.update_the_listings()

elif input == '2':
    print("update listing")
    Driver.insert_new_listings()

elif input == '3':
    print("update price")
    Driver.run_through_multi_day_cycle(5)

elif input == '4':
    print("clean")
    Components.clean_the_price()

elif input == '5':
    print("up_the_search")
    Driver.up_the_search_one_day()

else:
    print("somethingelse")
    Driver.print_url_for_each_neighbourhood()
