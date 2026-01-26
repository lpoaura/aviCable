export function getSafeRedirect(
  redirect: unknown,
  fallback: `/${string}` = '/'
): `/${string}` {
  if (typeof redirect !== 'string') {
    return fallback
  }

  // Supprime les espaces et caractères bizarres
  const trimmed = redirect.trim()

  // Doit être une route interne absolue
  if (!trimmed.startsWith('/')) {
    return fallback
  }

  // Blocage explicite des URLs externes déguisées
  if (
    trimmed.startsWith('//') ||
    trimmed.startsWith('/\\') ||
    trimmed.includes('://')
  ) {
    return fallback
  }

  return trimmed as `/${string}`
}