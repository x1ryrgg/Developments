# Developments

## This project contains small developments.

**1. Hierarchical tree-type structure.**

**2. Integration with openweather api for checking the weather in the city**

### URLS
**1.1 - tree/  - показывает все объекты**

**1.2 - child/<int:id>/  - выводит объекты, родителем которых является выбранный id**

**1.3 - drevo/<int:id>/  - выводит цепочка родителей каждого слеудующего объекта**

**2.1 - weather/?city-London - вместо 'London' можете ввести любой город и узнать там температуру**