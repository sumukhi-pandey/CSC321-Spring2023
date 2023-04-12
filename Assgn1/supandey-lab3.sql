-- Lab 3
-- supandey
-- Apr 26, 2022

USE `supandey`;
-- BAKERY-1
-- Using a single SQL statement, reduce the prices of Lemon Cake and Napoleon Cake by $2.
update goods
set Price = Price - 2.0
where (Flavor = 'Lemon'or Flavor = 'Napoleon') and Food = 'Cake';


USE `supandey`;
-- BAKERY-2
-- Using a single SQL statement, increase by 15% the price of all Apricot or Chocolate flavored items with a current price below $5.95.
update goods
set Price = Price + (0.15*Price)
where (Flavor = 'Apricot' or Flavor = 'Chocolate') and Price < 5.95;


USE `supandey`;
-- BAKERY-3
-- Add the capability for the database to record payment information for each receipt in a new table named payments (see assignment PDF for task details)
drop table if exists payments;
create table payments(
Receipt Varchar(10) not null,
Amount decimal(3,2) not null,
PaymentSettled DATETIME,
PaymentType Varchar(15) not null,
primary key(Amount, PaymentSettled),
foreign key (Receipt) references receipts(RNumber)
);

USE `supandey`;
-- BAKERY-4
-- Create a database trigger to prevent the sale of Meringues (any flavor) and all Almond-flavored items on Saturdays and Sundays.
create trigger preventsales before insert on items
for each row
begin
    DECLARE errorMessage VARCHAR(255);
        declare newflavor Varchar(100);
        declare newfood Varchar(100);
        declare newDay Varchar(100);
        
        select Flavor into newflavor from goods where GId = NEW.Item;
        select Food into newfood from goods where GId = NEW.Item;
        select DAYNAME(SaleDate) into newDay from receipts where RNumber = NEW.Receipt;
                            
        IF (newflavor = 'Almond' or newfood = 'Meringue') and (newDay = 'Saturday' or newDay = 'Sunday') THEN
            SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = 'The Partnership is Invalid';
        END IF;
end;


USE `supandey`;
-- AIRLINES-1
-- Enforce the constraint that flights should never have the same airport as both source and destination (see assignment PDF)
create trigger sameairport before insert on flights
for each row
begin
    DECLARE errorMessage VARCHAR(255);
        SET errorMessage = CONCAT('The Source Airport ',
                            NEW.SourceAirport,
                            ' cannot be the same as Destination Airport',
                            New.DestAirport);
                            
        IF NEW.SourceAirport = New.DestAirport THEN
            SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = errorMessage;
        END IF;
end;


USE `supandey`;
-- AIRLINES-2
-- Add a "Partner" column to the airlines table to indicate optional corporate partnerships between airline companies (see assignment PDF)
alter table airlines
add column Partner Varchar(20);

update airlines
set Partner = 'Southwest' where Abbreviation = 'JetBlue';

update airlines
set Partner = 'JetBlue' where Abbreviation = 'SouthWest';

drop trigger wrongpartner
create trigger wrongpartner before insert on airlines
for each row
begin
    DECLARE errorMessage VARCHAR(255);
        SET errorMessage = CONCAT('The Partnership is Invalid');
                            
        IF New.Abbreviation = NEW.Partner or New.Partner not in (select Abbreviation from airlines)THEN
            SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = errorMessage;
        END IF;
end;

drop trigger wrongpartner2
create trigger wrongpartner2 before update on airlines
for each row
begin
    DECLARE errorMessage VARCHAR(255);
        SET errorMessage = CONCAT('The Partnership is Invalid');
                            
        IF New.Partner in (select Partner from airlines)THEN
            SIGNAL SQLSTATE '45000' 
                SET MESSAGE_TEXT = errorMessage;
        END IF;
end;


USE `supandey`;
-- KATZENJAMMER-1
-- Change the name of two instruments: 'bass balalaika' should become 'awesome bass balalaika', and 'guitar' should become 'acoustic guitar'. This will require several steps. You may need to change the length of the instrument name field to avoid data truncation. Make this change using a schema modification command, rather than a full DROP/CREATE of the table.
update Instruments
set Instrument = 'awesome bass balalaika'
where Instrument = 'bass balalaika';

update Instruments
set Instrument = 'acoustic guitar'
where Instrument = 'guitar';


USE `supandey`;
-- KATZENJAMMER-2
-- Keep in the Vocals table only those rows where Solveig (id 1 -- you may use this numeric value directly) sang, but did not sing lead.
delete from Vocals
where (Bandmate = 1 and `Type` = 'lead') or (Bandmate != 1);


