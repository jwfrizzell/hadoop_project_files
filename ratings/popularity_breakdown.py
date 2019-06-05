from mrjob.job import MRJob
from mrjob.step import MRStep

class PopularityBreakdown(MRJob):
    def steps(self):
        return [
            MRStep(
                   mapper=self.mapper_get_popularity,
                   reducer=self.reducer_count_popularity
            ),
            MRStep(reducer=self.reducer_sort_popularity)
        ]

    def mapper_get_popularity(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield movieID,1

    def reducer_count_popularity(self, key, values):
        yield str(sum(values)).zfill(5),int(key)

    def reducer_sort_popularity(self,count, movies):
        for movie in movies:
            yield movie, count

if __name__ == '__main__':
    PopularityBreakdown.run()


