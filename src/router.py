"""Module with routes."""

import logging

from fastapi import APIRouter, HTTPException, Request

from src.codec import decode, encode
from src.hmac_service import HMACSigner
from src.models import SignRequest, SignResponse, VerifyRequest, VerifyResponse

logger = logging.getLogger(__name__)
router = APIRouter()


def _get_signer(request: Request) -> HMACSigner:
    return request.app.state.signer


@router.post('/sign')
async def sign(request: Request, body: SignRequest) -> SignResponse:
    """Sign handler - creates HMAC signature for message."""
    max_size = request.app.state.settings.max_msg_size_bytes

    if len(body.msg.encode('utf-8')) > max_size:
        raise HTTPException(
            status_code=413, detail='Message exceeds maximum size'
        )

    try:
        signer = _get_signer(request)
        signature_bytes = signer.sign(body.msg)
        return SignResponse(signature=encode(signature_bytes))
    except Exception as e:
        logger.error('Error signing message: %s', str(e))
        raise HTTPException(status_code=500, detail='internal')


@router.post('/verify')
async def verify(request: Request, body: VerifyRequest) -> VerifyResponse:
    """Verify message with signature handler."""
    max_size = request.app.state.settings.max_msg_size_bytes

    if len(body.msg.encode('utf-8')) > max_size:
        raise HTTPException(
            status_code=413, detail='Message exceeds maximum size'
        )

    try:
        signer = _get_signer(request)
        signature_bytes = decode(body.signature)
        is_valid = signer.verify(body.msg, signature_bytes)
        return VerifyResponse(ok=is_valid)
    except ValueError:
        raise HTTPException(status_code=400, detail='invalid_signature_format')
    except Exception as e:
        logger.error('Error verifying signature: %s', str(e))
        raise HTTPException(status_code=500, detail='internal')
