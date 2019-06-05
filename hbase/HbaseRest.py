import sys
from starbase import Connection

def main(args=None):
    try:
        c = Connection('127.0.0.1', '8000')

        ratings = c.table('ratings')

        if ratings.exists():
            print("Dropping existing ratings table\n")
            ratings.drop()

        #Create column family called rating.
        ratings.create('rating')

        print('Parsing the ml-100k ratings data...\n')
        with open('/Users/joefrizzell/Downloads/ml-100k/u.data','r') as f:
            batch = ratings.batch()
            for line in f:
                (userID,movieID,rating,_) = line.split()
                batch.update(userID,{'rating':{movieID: rating}})
            print('Commiting ratings data to HBase via REST service.\n')
            batch.commit(finalize=True)

        print('Get back ratings for some users...\n')
        print('Ratings for user ID 1: {0}'.format(ratings.fetch('1')))
        print('Ratings for user ID 33: {0}'.format(ratings.fetch('33')))
    except Exception as ex:
        print("HBase Error: {0}".format(ex))
    

if __name__=="__main__":
    main(sys.argv[1:])