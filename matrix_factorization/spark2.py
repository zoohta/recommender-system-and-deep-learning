from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
from pyspark import SparkContext

sc = SparkContext('local', 'AlsSpark')

data = sc.textFile('/Users/kohtaasakura/PyDev/recsys_deep_learning/movielens_data/very_small_rating.csv')

# filter out header
header = data.first()  # extract header
data = data.filter(lambda row: row != header)

# convert into a sequence of Rating objects
ratings = data.map(lambda l: l.split(',')).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

# split into train and test
train, test = ratings.randomSplit([0.8, 0.2])

# train the model
K = 10
epochs = 10
model = ALS.train(train, K, epochs)

# evaluate the model

# train
x = train.map(lambda p: (p[0], p[1]))
p = model.predictAll(x).map(lambda r: ((r[0], r[1]), r[2]))
ratesAndPreds = train.map(lambda r: ((r[0], r[1]), r[2])).join(p)
# joins on first item: (user_id, movie_id)
# each row of result is: ((user_id, movie_id), (rating, prediction))
mse = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("train mse: %s" % mse)

# test
x = test.map(lambda p: (p[0], p[1]))
p = model.predictAll(x).map(lambda r: ((r[0], r[1]), r[2]))
ratesAndPreds = test.map(lambda r: ((r[0], r[1]), r[2])).join(p)
mse = ratesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("test mse: %s" % mse)