% Recommendation Rules

% This file contains the rules/logic for recommending games based on various criteria
% Format: game(Title, Genre, Platform, Rating)

% recommend_by_genre(PlayedGame, RecommendedGame)
% Recommends games that share the same genre as the played game
% Arg:
%   PlayedGame: The game the user has played
%   RecommendedGame: A recommended game with the same genre
recommend_by_genre(PlayedGame, RecommendedGame) :-
    game(PlayedGame, Genre, _, _),
    game(RecommendedGame, Genre, _, _),
    PlayedGame \= RecommendedGame.

% recommend_by_platform(PlayedGame, RecommendedGame)
% Recommends games available on the same platform
% Args:
%   PlayedGame: The game the user has played
%   RecommendedGame: A recommended game on the same platform
recommend_by_platform(PlayedGame, RecommendedGame) :-
    game(PlayedGame, _, Platform, _),
    game(RecommendedGame, _, Platform, _),
    PlayedGame \= RecommendedGame.

% recommend_highly_rated(RecommendedGame, MinRating)
% Recommends games with rating above threshold
% Args:
%   RecommendedGame: A highly rated game
%   MinRating: Minimum rating threshold
recommend_highly_rated(RecommendedGame, MinRating) :-
    game(RecommendedGame, _, _, Rating),
    Rating >= MinRating.

% recommend_similar(PlayedGame, RecommendedGame)
% Recommends games similar to the played game (same genre AND high rating)
% Args:
%   PlayedGame: The game the user has played
%   RecommendedGame: A recommended similar game
recommend_similar(PlayedGame, RecommendedGame) :-
    game(PlayedGame, Genre, _, PlayedRating),
    game(RecommendedGame, Genre, _, RecRating),
    PlayedGame \= RecommendedGame,
    RecRating >= PlayedRating - 10.  % Within 10 points of played game's rating

% recommend_best_match(PlayedGame, RecommendedGame)
% Best recommendation: same genre, same platform, similar rating
% Args:
%   PlayedGame: The game the user has played
%   RecommendedGame: The best matching recommendation
recommend_best_match(PlayedGame, RecommendedGame) :-
    game(PlayedGame, Genre, Platform, PlayedRating),
    game(RecommendedGame, Genre, Platform, RecRating),
    PlayedGame \= RecommendedGame,
    RecRating >= PlayedRating - 15.  % Within 15 points