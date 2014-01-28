print("Loading...")
users <- read.table('../parsed/1kusers.tsv', header=TRUE, sep="\t", quote="", comment.char="")
#users <- read.table('../parsed/parsedProfiles.tsv', header=TRUE, sep="\t", quote="", comment.char="")
ratings <- read.table('../parsed/parsedRatings.tsv', header=TRUE, sep="\t", quote="", comment.char="")
recipes <- read.table('../parsed/parsedRecipes.tsv', header=TRUE, sep="\t", quote="", comment.char="")
ingredients <- read.table('../parsed/parsedIngredients.tsv', header=TRUE, sep="\t", quote="", comment.char="")

#hobbies <- read.table('../parsed/hobbies.tsv', header=TRUE, sep="\t", quote="", comment.char="")
#interests <- read.table('../parsed/interest.tsv', header=TRUE, sep="\t", quote="", comment.char="")
print("Finished loading")


print("Filtering out non-US users and users without a state")
ususers = users[ which(users$livingcountry == " USA" & users$livingstate != ""),]



print("Merging recipes + ingredients")
recipes_ing <- merge(recipes, ingredients, by=c("recID"))

print("Merging users and ratings")
#users.filtered <- users[users$livingcountry == " USA"]
user_ratings <- merge(ususers, ratings, by=c("uid"))

# never do this, 20+gb RAM
#all_merged <- merge(recipes_ing, user_ratings, by.x="recID", by.y="recid")

N=10
#cat("State\tTown\trecipeID\tingrID")

print("Merging per state")
states <- unique(ususers$livingstate)
for (state in states){
	if(state == ""){
		print("should not happen")
		next
	}
	print(paste("Merging user and ratings for state ", state, sep=""))
	# keeping only ratings from a particular state
	user_ratings.state <- user_ratings[user_ratings$livingstate==state,]
	towns <- unique(user_ratings.state$livingtown)
	for (town in towns){
		if (nchar(town) < 3){
			next
		}
		user_ratings.town <- user_ratings.state[user_ratings.state$livingtown==town,]
		#merge ratings with ingredients, by town in state
		town.full <- merge(recipes_ing, user_ratings.town, by.x="recID", by.y="recid")
		town.state.df <- data.frame(s=town.full$siteID, recID=town.full$recID)
		town.state.all.agg <- aggregate(recID ~ s, data=town.state.df, FUN=length)
		town.state.sorted.indices <- order(town.state.all.agg$recID, decreasing=T)
		counts <- town.state.all.agg$recID[town.state.sorted.indices][1:N]
		ingredients <- town.state.all.agg$s[town.state.sorted.indices][1:N]
		for (i in town.state.sorted.indices[1:N]){
		cat(state, town, town.state.all.agg$recID[i], town.state.all.agg$s[i], file="townCounts.tsv", append=TRUE, '\n', sep="\t")
		} 
#		break
	}
#	break


	# merge with recipes and the smaller/filtered states table
#	state.all <- merge(recipes_ing, user_ratings.state, by.x="recID", by.y="recid")

	#print(head(state.all, 1))
	# small data frame with only two columns: ingredient id (siteID) and another column (irrelevant)
#	state.all.df <- data.frame(s=state.all$siteID, r=state.all$recID)
#	state.all.agg <- aggregate(r ~ s, data=state.all.df, FUN=length)
#	sorted.indices <- order(state.all.agg$r, decreasing=T)
#	counts <- state.all.agg$r[sorted.indices][1:N]
#	ingredients <- state.all.agg$s[sorted.indices][1:N]
#	for (i in sorted.indices[1:N]){
#		cat(state, state.all.agg$s[i], state.all.agg$r[i], '\n', sep="\t")
#	}
#	break
}
