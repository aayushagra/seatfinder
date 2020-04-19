class WelcomeController < ApplicationController
  def index
    @recommended_seats = ''
    if params.has_key?(:title)
      @recommended_seats = %x[node main.ts #{params[:numseats]} #{params[:title]}]
    end

    movies = Dir["movies/*.json"]
    @movies_data = []
    for i in movies
      file = File.open i
      data = JSON.load file
      @movies_data.push(data)
    end
  end
  
  def intToChar(i, j)
    return (i+97).chr + (j+1).to_s
  end

  def createmovie
    require 'json'

    moviename = params[:moviename]
    rows = params[:numrows]
    cols = params[:numcols]
    summary = params[:summary]
    genre = params[:genre]
    year = params[:year]
    imdb = params[:imdb]

    final = Hash[
      "title" => moviename,
      "summary" => summary,
      "genre" => genre,
      "year" => year,
      "imdb" => imdb,
      "venue" => Hash[
        "layout" => Hash[
          "rows" => rows,
          "columns" => cols
        ]
      ],
      "seats" => Hash.new
    ]

    for i in 0..(Integer(rows)-1)
      for j in 0..(Integer(cols)-1)
        seatId = intToChar(i, j)
        final["seats"][seatId] = Hash[
          "id": seatId,
          "row": seatId[0],
          "column": seatId[1],
          "status": "AVAILABLE"
        ]
      end
    end

    File.open("movies/#{moviename}.json", "w") do |f|     
      f.write(final.to_json)   
    end
  end
end
