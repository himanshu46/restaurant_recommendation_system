db.restaurants.update( {},
    [{ $set: { coordinates: ["$longitude","$latitude"] } }],
    { multi: true })



db.restaurants.createIndex( { coordinates : "2dsphere" } )


 db.restaurants.find({
    coordinates: {
        $geoNear: {
            $geometry: {
                type: 'Point',
                coordinates: [
                    77.685181,
                    12.932102
                ]
            },
            $maxDistance: 20000
        }
    }
}).pretty()


db.restaurants.drop()