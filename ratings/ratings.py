from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingsBreakdown(MRJob):
    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_get_ratings,
                reducer=self.reducer_count_ratings
            )
        ]

    def mapper_get_ratings(self, _, line):
        '''
        Split the value in the line passed by caller and
        get the rating value as key. Set the key value to 
        1 meaning for each rating we have one instance of 
        that rating.
        FE: If we had a ratings of 3,4 and 5 it would look like
        {3:1,4:1,5:1}
        '''
        (user_id, movie_id, rating, timestamp) = line.split('\t')
        yield rating, 1

    def reducer_count_ratings(self, key, value):
        '''
        Take each rating and sum the values. All values
        will account for one value. 
        FE: if we had ratings 3 5 times the final output
        would resemble the following. 
        {3:5}
        '''
        yield key, sum(value)

if __name__=="__main__":
    RatingsBreakdown.run()