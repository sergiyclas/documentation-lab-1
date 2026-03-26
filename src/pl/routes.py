"""Presentation Layer - FastAPI routes"""

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from src.dal import get_db, DataAccessService
from src.bll import SpotifyService, StatisticsService
from src.common.logger import get_logger
from src.pl.schemas import (
    UserResponse,
    SongResponse,
    PlaylistSummary,
    StatisticsResponse,
    ImportResponse,
)

router = APIRouter(prefix="/api", tags=["spotify"])
logger = get_logger(__name__)


# Dependency: Get SpotifyService
def get_spotify_service(db: Session = Depends(get_db)) -> SpotifyService:
    """Dependency injection for SpotifyService"""
    dal = DataAccessService(db)
    return SpotifyService(dal)


# Dependency: Get StatisticsService
def get_statistics_service(db: Session = Depends(get_db)) -> StatisticsService:
    """Dependency injection for StatisticsService"""
    dal = DataAccessService(db)
    return StatisticsService(dal)


# ==================== Import Routes ====================


@router.post("/import/csv", response_model=ImportResponse)
async def import_csv(
    file: UploadFile = File(...), service: SpotifyService = Depends(get_spotify_service)
):
    """
    Import data from CSV file

    CSV format: email, subType, playlistName, songTitle, artist, duration, genre
    """
    try:
        import tempfile
        import os

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Import from temporary file
            stats = await service.import_csv(tmp_path)

            logger.info(f"CSV import successful: {stats}")
            return ImportResponse(
                status="success",
                message=f"Successfully imported {stats.get('total_rows', 0)} rows",
                statistics=stats,
            )
        finally:
            # Clean up temporary file
            os.remove(tmp_path)

    except Exception as e:
        logger.error(f"Error importing CSV: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== User Routes ====================


@router.get("/users")
async def get_all_users(service: SpotifyService = Depends(get_spotify_service)):
    """Get all users on the platform"""
    try:
        users = await service.get_all_users()
        user_responses = [
            {
                "id": u.id,
                "email": u.email,
                "username": u.username,
                "subscription_type": u.subscription.type,
                "registration_date": u.registration_date.isoformat(),
            }
            for u in users
        ]
        return {"status": "success", "count": len(user_responses), "data": user_responses}
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}")
async def get_user_detail(user_id: int, service: SpotifyService = Depends(get_spotify_service)):
    """Get user details including their playlists"""
    try:
        user_data = await service.get_user_with_playlists(user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success", "data": user_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Song Routes ====================


@router.get("/songs")
async def get_all_songs(service: SpotifyService = Depends(get_spotify_service)):
    """Get all songs in the platform"""
    try:
        songs = await service.get_all_songs()
        song_responses = [
            {
                "id": s.id,
                "title": s.title,
                "artist": s.artist,
                "duration": s.duration,
                "genre": s.genre,
                "created_at": s.created_at.isoformat(),
            }
            for s in songs
        ]
        return {"status": "success", "count": len(song_responses), "data": song_responses}
    except Exception as e:
        logger.error(f"Error retrieving songs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Playlist Routes ====================


@router.get("/playlists")
async def get_all_playlists(service: SpotifyService = Depends(get_spotify_service)):
    """Get all playlists on the platform"""
    try:
        playlists = await service.get_all_playlists()
        playlist_responses = [
            {
                "id": p.id,
                "name": p.name,
                "owner_id": p.owner_id,
                "song_count": len(p.songs),
                "created_at": p.created_at.isoformat(),
            }
            for p in playlists
        ]
        return {"status": "success", "count": len(playlist_responses), "data": playlist_responses}
    except Exception as e:
        logger.error(f"Error retrieving playlists: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/playlists/{playlist_id}")
async def get_playlist_detail(
    playlist_id: int, service: SpotifyService = Depends(get_spotify_service)
):
    """Get playlist details including all songs"""
    try:
        playlist_data = await service.get_playlist_with_songs(playlist_id)
        if not playlist_data:
            raise HTTPException(status_code=404, detail="Playlist not found")
        return {"status": "success", "data": playlist_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving playlist {playlist_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Statistics Routes ====================


@router.get("/statistics")
async def get_statistics(service: StatisticsService = Depends(get_statistics_service)):
    """Get platform statistics (users, songs, playlists, subscriptions)"""
    try:
        stats = await service.get_statistics()
        return {"status": "success", "data": stats}
    except Exception as e:
        logger.error(f"Error retrieving statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Health Check ====================


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}
