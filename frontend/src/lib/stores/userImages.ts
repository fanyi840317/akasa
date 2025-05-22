import { writable } from 'svelte/store';
import { databases } from '../../../../web.app/src/lib/appwrite'; // Import databases from shared appwrite client
import { ID, Query } from 'appwrite';
import type { Models } from 'appwrite';

// Import appwrite config for database and collection IDs
import { appwriteConfig } from '../../../../web.app/src/lib/appwrite';
const { databaseId } = appwriteConfig;

// Define user images collection ID
const userImagesCollectionId = 'user_images'; // Assuming a collection named 'user_images'

interface UserImage extends Models.Document {
  userId: string;
  provider?: string; // 图片提供者 (e.g., 'upload', 'unsplash', 'pexels')
  imageUrl: string; // 原始图片URL
  thumbnailUrl?: string; // 缩略图URL
  extraData?: string; // 存储额外数据，如API提供者的元数据
}

type UserImagesState = {
    images: UserImage[];
    listLoading: boolean;
    error: string | null;
};

const createUserImagesStore = () => {
    const { subscribe, set, update } = writable<UserImagesState>({
        images: [],
        listLoading: false,
        error: null
    });

    return {
        subscribe,
        // Function to load user images from Appwrite
        loadUserImages: async (userId: string) => {
            console.log(`userImages.ts: loadUserImages: Starting image load for userId: ${userId}`); // Existing log
            update(state => ({ ...state, listLoading: true, error: null }));
            try {
                const response = await databases.listDocuments(
                    databaseId,
                    userImagesCollectionId,
                    [Query.equal('userId', userId)]
                );
                console.log('userImages.ts: loadUserImages: Documents fetched:', response.documents); // Existing log
                const loadedImages = response.documents as UserImage[];
                console.log('userImages.ts: loadUserImages: MAPPED loadedImages before update:', JSON.stringify(loadedImages));

                update(state => {
                    console.log('userImages.ts: loadUserImages: INSIDE update callback, current store state before merge:', JSON.stringify(state));
                    console.log('userImages.ts: loadUserImages: INSIDE update callback, new loadedImages to set:', JSON.stringify(loadedImages));
                    const newState = {
                        ...state,
                        images: loadedImages, // Ensure this is a new array reference if loadedImages is different
                        listLoading: false
                    };
                    console.log('userImages.ts: loadUserImages: INSIDE update callback, newState to be set:', JSON.stringify(newState));
                    return newState;
                });
                // Log after update to see the store's state if possible, though direct access isn't typical here
                // We rely on subscription or $derived in components to see the change.
                console.log(`userImages.ts: loadUserImages: Update call completed for userId: ${userId}. Check component logs for $derived updates.`);
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Failed to load user images';
                update(state => ({ ...state, listLoading: false, error: errorMessage }));
                console.error('Error loading user images:', error);
                throw error; // Re-throw to allow components to handle
            }
        },

        // Function to add a new image URL to Appwrite
        addUserImage: async (userId: string, imageUrl: string, provider?: string, thumbnailUrl?: string, extraData?: unknown, deleteUrl?: string) => {
            update(state => ({ ...state, listLoading: true, error: null })); // Use listLoading for simplicity, could add specific addLoading
            try {
                const response = await databases.createDocument(
                    databaseId,
                    userImagesCollectionId,
                    ID.unique(),
                    { userId, imageUrl, provider, thumbnailUrl, extraData: JSON.stringify({ ...(extraData ? extraData : {}), deleteUrl }) }
                );
                const newUserImage = response as UserImage;
                update(state => ({
                    ...state,
                    images: [...state.images, newUserImage],
                    listLoading: false
                }));
                return newUserImage;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Failed to add user image';
                update(state => ({ ...state, listLoading: false, error: errorMessage }));
                console.error('Error adding user image:', error);
                throw error; // Re-throw to allow components to handle
            }
        },

        // Function to remove an image from Appwrite
        removeUserImage: async (imageId: string) => {
            update(state => ({ ...state, listLoading: true, error: null })); // Use listLoading for simplicity, could add specific removeLoading
            try {
                await databases.deleteDocument(
                    databaseId,
                    userImagesCollectionId,
                    imageId
                );
                update(state => ({
                    ...state,
                    images: state.images.filter(img => img.$id !== imageId),
                    listLoading: false
                }));
                return true;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : 'Failed to remove user image';
                update(state => ({ ...state, listLoading: false, error: errorMessage }));
                console.error('Error removing user image:', error);
                throw error; // Re-throw to allow components to handle
            }
        },

        // Clear error state
        clearError: () => {
            update(state => ({ ...state, error: null }));
        },

        // Reset state
        reset: () => {
            console.log('userImages.ts: reset: Resetting store');
            set({
                images: [],
                listLoading: false,
                error: null
            });
            console.log('userImages.ts: reset: Store has been reset');
        },
    };
};

// Export the factory function
export const userImagesStore = createUserImagesStore();