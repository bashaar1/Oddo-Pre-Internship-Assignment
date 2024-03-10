Understand the folder structure
Initialized the module named as "Real-Estate Management" create the file__init__.py,__manifest__.py,models,data,security and views
make this module an app by making the 'appication':True in the __manifest__.py file
created the model:
1. estate_property_model.py
	Add the required fields into the models as given in the file

created a data file
gave access rights of the model file in the security/ir.model.access.csv
specify the actions for the model estate.model
link that action to the specify menu
created views for the model like Tree view , form view and serch view also add the filter and group by to the search
created a new model
2. estate_property_type_model.py
	this model has the type for the property and we have created a relation Many2one with this model for e.g estate.property has a Many2one relation with estate_property_type_model model by doing this a property can have 1 type and the same type can be assigned to multiple types
 after this model i defined the two more fields with the model res.partner who is the buyer
 and the next one is the res.user
 
create a new model:
3. estate_property_tag.py
	this model has the Many2many relation this means that the multiple properties can have multiple tags and the multiple tag can have the multiple properties

create a new model	
4. real_estate_property_offer.py
now the estate.property has a relation One2many with the real_estate_property_offer model this will insure that the 1 property can have the many offer and the many offer can be given to one property

Added the desired computed fields
Added the onchange function for the garden field that the garden_area will have the value(10) and the garden_orientation will have the value north
Added the buttons and their function "Cancel" , "Sold"
Added the Sql Constrains to ensure data consistency
Added the Python Constraint to create more complex constraints

